"""Перевод английских глосс KANJIDIC2 на русский в черновик для вычитки.

Запуск (с хоста, не в контейнере — ключу нечего делать в образе):

    python3 -m venv .venv && . .venv/bin/activate
    pip install -r requirements-scripts.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    python -m scripts.etl.translate_meanings --limit 30

ЧТО ЭТО НЕ ДЕЛАЕТ. Скрипт не выводит значение иероглифа и не решает, что
показать пользователю. Он переводит уже готовые словарные глоссы: «book» →
«книга». Результат кладётся в data/kanji_ru_draft.json и НИКОГДА не попадает
в поле meaning — туда значение переносит человек через review_meanings.py.
Флаг is_published по-прежнему зависит только от ручной вычитки.

Разделение не формальное. Попытка вывести значение автоматически (из словарных
статей) давала правдоподобную ложь: 山 → «спекуляция», 本 → «счётный суффикс».
Перевод готовой глоссы — принципиально более простая и надёжная операция, но
доверия к публикации без человека он всё равно не даёт: у 張 первая глосса
KANJIDIC — «counter for bows & stringed instruments», и «правильного» значения
там просто нет без выбора.

УСТОЙЧИВОСТЬ. Черновик — накопитель, а не результат одного прогона: скрипт
стартует с чтения существующего файла и пропускает всё, что там уже есть.
Каждый батч дописывается на диск сразу, атомарной заменой файла. Падение,
Ctrl-C или разрыв сети теряют максимум один текущий батч.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

from scripts.build_dataset import load_jlpt_list, load_kanjidic

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DRAFT_FILE = DATA_DIR / "kanji_ru_draft.json"
OVERRIDES_FILE = DATA_DIR / "kanji_ru.json"

# Опус выбран сознательно: это контент, который потом читает живой человек, и
# каждая неточность здесь оплачивается его временем на вычитке. Полный прогон
# по 2055 знакам стоит несколько долларов — экономить тут нечего.
DEFAULT_MODEL = "claude-opus-5"
DEFAULT_BATCH_SIZE = 30

SYSTEM_PROMPT = """\
Ты переводишь на русский готовые английские глоссы иероглифов из словаря \
KANJIDIC2. Это перевод коротких словарных статей, а не толкование иероглифа: \
переводи то, что написано в глоссе, ничего не добавляя от себя и не исправляя \
источник.

Правила перевода:
- 1–4 слова на глоссу, без пояснений в скобках, без артиклей и вводных слов;
- строчная буква, если это не имя собственное;
- каждой английской глоссе соответствует ровно одна русская, в том же \
порядке; ничего не пропускай, не объединяй и не переставляй;
- чтения он/кун даны только для снятия омонимии, переводить их не нужно.

Каждой глоссе проставь kind:
- "special" — если это не обычное значение слова: счётные суффиксы \
("counter for ..."), знаки китайского зодиака и связанные с ними часы \
("sign of the rat", "11PM-1AM"), названия ключей ("... radical (no. 63)"), \
пометы вроде "-times" или "un-", устаревшие и узкоспециальные значения;
- "primary" — во всех остальных случаях.

Порядок глосс в KANJIDIC не гарантирует, что первая из них основная: у 張 \
первой идёт "counter for bows & stringed instruments", хотя основное значение \
знака — "натягивать". Определяй kind по смыслу самой глоссы, а не по позиции.
"""

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "character": {"type": "string"},
                    "meanings": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "en": {"type": "string"},
                                "ru": {"type": "string"},
                                "kind": {
                                    "type": "string",
                                    "enum": ["primary", "special"],
                                },
                            },
                            "required": ["en", "ru", "kind"],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["character", "meanings"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["items"],
    "additionalProperties": False,
}

# Сколько основных значений склеивается в готовую строку для поля meaning.
# Больше трёх — это уже не значение, а список, который человек всё равно
# сократит на вычитке.
MAX_PRIMARY_IN_MEANING = 3


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# Черновик на диске
# --------------------------------------------------------------------------


def load_draft() -> dict[str, dict]:
    if not DRAFT_FILE.exists():
        return {}
    rows = json.loads(DRAFT_FILE.read_text(encoding="utf-8"))
    return {row["character"]: row for row in rows}


def save_draft(draft: dict[str, dict]) -> None:
    """Атомарная запись: временный файл рядом плюс os.replace.

    Обычный open(path, "w") усекает файл в момент открытия. Падение посреди
    сериализации нескольких мегабайт оставило бы обрезанный JSON, то есть
    уничтожило бы ВСЮ накопленную работу, а не только текущий батч.
    os.replace атомарен в пределах файловой системы: на диске всегда лежит
    либо целиком старая версия, либо целиком новая.
    """
    rows = sorted(draft.values(), key=lambda r: r["order_index"])
    tmp = DRAFT_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, DRAFT_FILE)


# --------------------------------------------------------------------------
# Подготовка задания
# --------------------------------------------------------------------------


def build_queue(limit: int | None) -> list[dict]:
    """Знаки, которым нужен перевод, по возрастанию order_index.

    Пропускаются уже вычитанные вручную (там значение есть и оно лучше) и уже
    переведённые (на этом держится возобновление после сбоя).
    """
    kanjidic = load_kanjidic()
    jlpt = load_jlpt_list()

    manual = set()
    if OVERRIDES_FILE.exists():
        manual = {
            row["character"]
            for row in json.loads(OVERRIDES_FILE.read_text(encoding="utf-8"))
            if row.get("meaning")
        }
    done = set(load_draft())

    queue: list[dict] = []
    for position, row in enumerate(
        sorted(jlpt, key=lambda r: r.get("frequency") or 10**6), 1
    ):
        char = row["kanji"]
        if char in manual or char in done:
            continue
        kd = kanjidic.get(char) or {}
        glosses = [g for g in (kd.get("meaning_en") or []) if g]
        if not glosses:
            continue
        queue.append(
            {
                "character": char,
                "order_index": position,
                "glosses": glosses,
                "kun": (kd.get("kun") or [None])[0],
                "on": (kd.get("on") or [None])[0],
            }
        )

    return queue[:limit] if limit else queue


def build_user_message(batch: list[dict]) -> str:
    payload = [
        {
            "character": item["character"],
            "meanings_en": item["glosses"],
            "kun_reading": item["kun"],
            "on_reading": item["on"],
        }
        for item in batch
    ]
    return (
        "Переведи глоссы для этих иероглифов.\n\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
    )


# --------------------------------------------------------------------------
# Разбор и проверка ответа
# --------------------------------------------------------------------------


class BatchInvalid(Exception):
    """Ответ пришёл, но не соответствует заданию."""


def parse_response(text: str, batch: list[dict]) -> dict[str, list[dict]]:
    """Разбирает ответ и сверяет его с отправленным заданием.

    Проверка глосс побайтово — не педантизм. Модель может переписать или
    переставить английский оригинал, и тогда перевод поедет относительно
    исходного списка. На вычитке такое расхождение всплыло бы уже как
    непонятная ошибка в контенте, а здесь ловится сразу.
    """
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise BatchInvalid(f"ответ не разбирается как JSON: {exc}") from exc

    items = data.get("items")
    if not isinstance(items, list):
        raise BatchInvalid("в ответе нет массива items")

    expected = {item["character"]: item["glosses"] for item in batch}
    result: dict[str, list[dict]] = {}

    for entry in items:
        char = entry.get("character")
        if char not in expected:
            raise BatchInvalid(f"в ответе лишний иероглиф {char!r}")
        meanings = entry.get("meanings") or []
        want = expected[char]
        if len(meanings) != len(want):
            raise BatchInvalid(
                f"{char}: значений {len(meanings)}, а глосс было {len(want)}"
            )
        for got, source in zip(meanings, want, strict=True):
            if got.get("en") != source:
                raise BatchInvalid(
                    f"{char}: глосса изменена — {got.get('en')!r} вместо {source!r}"
                )
            if not (got.get("ru") or "").strip():
                raise BatchInvalid(f"{char}: пустой перевод для {source!r}")
        result[char] = meanings

    missing = set(expected) - set(result)
    if missing:
        raise BatchInvalid(f"в ответе нет иероглифов: {''.join(sorted(missing))}")

    return result


def compose_meaning_ru(meanings: list[dict]) -> str | None:
    """Готовая строка для поля meaning — только основные значения.

    Если основных нет вовсе (у 箇 единственная глосса — «counter for
    articles»), возвращается None: такую запись нельзя предложить к публикации
    одним нажатием, решение остаётся за человеком.
    """
    primary = [m["ru"].strip() for m in meanings if m.get("kind") == "primary"]
    if not primary:
        return None
    return "; ".join(primary[:MAX_PRIMARY_IN_MEANING])


# --------------------------------------------------------------------------
# Запрос
# --------------------------------------------------------------------------


def translate_batch(client, model: str, batch: list[dict]) -> dict[str, list[dict]]:
    response = client.messages.create(
        model=model,
        max_tokens=16000,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                # Промпт неизменен между батчами, поэтому кэшируется и со
                # второго запроса стоит примерно десятую часть.
                "cache_control": {"type": "ephemeral"},
            }
        ],
        output_config={
            # Механический перевод коротких глосс — ровно тот случай, для
            # которого низкий effort и предназначен.
            "effort": "low",
            "format": {"type": "json_schema", "schema": RESPONSE_SCHEMA},
        },
        messages=[{"role": "user", "content": build_user_message(batch)}],
    )

    if response.stop_reason == "refusal":
        raise BatchInvalid("модель отклонила запрос")
    if response.stop_reason == "max_tokens":
        raise BatchInvalid("ответ обрезан по max_tokens — уменьшите --batch-size")

    text = next((b.text for b in response.content if b.type == "text"), None)
    if text is None:
        raise BatchInvalid("в ответе нет текстового блока")
    return parse_response(text, batch)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, help="сколько знаков перевести за прогон")
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="показать первый батч и выйти, не обращаясь к API",
    )
    args = parser.parse_args()

    queue = build_queue(args.limit)
    if not queue:
        log("переводить нечего: всё либо вычитано вручную, либо уже в черновике")
        return

    batches = [
        queue[i : i + args.batch_size] for i in range(0, len(queue), args.batch_size)
    ]
    log(f"к переводу {len(queue)} знаков, батчей {len(batches)}, модель {args.model}")

    if args.dry_run:
        log("\n--- системный промпт ---")
        print(SYSTEM_PROMPT)
        log("--- первый батч ---")
        print(build_user_message(batches[0]))
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        log("ОШИБКА: не задан ANTHROPIC_API_KEY")
        raise SystemExit(1)

    import anthropic

    # Ретраи по 429 и 5xx с экспоненциальной паузой делает сам SDK; свой цикл
    # ниже нужен для ошибок содержания, где повтор осмыслен по другой причине.
    client = anthropic.Anthropic(max_retries=5)

    draft = load_draft()
    started_with = len(draft)
    translated = skipped = 0

    for number, batch in enumerate(batches, 1):
        chars = "".join(item["character"] for item in batch)
        log(f"[{number}/{len(batches)}] {chars}")

        meanings_by_char = None
        for attempt in (1, 2):
            try:
                meanings_by_char = translate_batch(client, args.model, batch)
                break
            except BatchInvalid as exc:
                log(f"  негодный ответ ({exc})" + (" — повторяю" if attempt == 1 else ""))
            except Exception as exc:  # noqa: BLE001 — сеть, 429, 5xx после ретраев SDK
                log(f"  сбой запроса: {type(exc).__name__}: {exc}")
                if attempt == 1:
                    time.sleep(20)

        if meanings_by_char is None:
            log(f"  ПРОПУСК батча: {chars}")
            skipped += len(batch)
            continue

        now = datetime.now(UTC).isoformat(timespec="seconds")
        for item in batch:
            char = item["character"]
            meanings = meanings_by_char[char]
            draft[char] = {
                "character": char,
                "order_index": item["order_index"],
                "meanings": meanings,
                "meaning_ru": compose_meaning_ru(meanings),
                "source": {
                    "meaning_en": item["glosses"],
                    "kun_reading_kana": item["kun"],
                    "on_reading_kana": item["on"],
                },
                "model": args.model,
                "translated_at": now,
            }
            translated += 1

        # Пишем после КАЖДОГО батча: цена — доли секунды, страховка — от
        # потери всего прогона.
        save_draft(draft)

    log("")
    log(f"переведено за прогон: {translated}")
    log(f"пропущено (негодный ответ или сбой): {skipped}")
    log(f"в черновике всего: {len(draft)} (было {started_with})")
    if skipped:
        log("пропущенные знаки подберёт следующий запуск — они не попали в черновик")


if __name__ == "__main__":
    main()
