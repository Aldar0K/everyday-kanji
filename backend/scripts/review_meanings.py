"""Консольный помощник вычитки машинного перевода значений.

Запуск:

    python -m scripts.review_meanings              # с начала очереди
    python -m scripts.review_meanings --from 300   # с order_index 300

Показывает по одному знаку: сам иероглиф, английские глоссы, машинный перевод
и чтения. Принятое значение сразу дописывается в data/kanji_ru.json — тот
самый файл, из которого build_dataset.py берёт поле meaning. То есть принять
значение здесь означает опубликовать знак после ближайшей пересборки.

Скрипт НИЧЕГО не решает сам: без явного нажатия в kanji_ru.json ничего не
попадает. Существующие записи файла не трогаются и не переупорядочиваются —
новые дописываются в конец, поэтому диff читается как чистое добавление.

Дописывание идёт после каждого принятого знака, а не в конце сессии: вычитка
двух тысяч значений — работа на много заходов, и терять её из-за закрытого
терминала нельзя.
"""

from __future__ import annotations

import argparse
import json
import os
import readline  # noqa: F401 — даёт редактирование строки в input()
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DRAFT_FILE = DATA_DIR / "kanji_ru_draft.json"
OVERRIDES_FILE = DATA_DIR / "kanji_ru.json"

HELP = """
  Enter / a  принять показанное значение
  e          отредактировать перед принятием
  s          пропустить (вернётся в следующий раз)
  q          выйти
"""


def _input_with_default(prompt: str, default: str) -> str:
    """input() с уже подставленным текстом, который можно править."""

    def hook() -> None:
        readline.insert_text(default)
        readline.redisplay()

    readline.set_startup_hook(hook)
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()


def load_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def append_override(row: dict) -> None:
    """Дописывает запись в конец kanji_ru.json атомарной заменой файла."""
    rows = load_rows(OVERRIDES_FILE)
    rows.append(row)
    tmp = OVERRIDES_FILE.with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(tmp, OVERRIDES_FILE)


def format_entry(entry: dict) -> str:
    lines = []
    source = entry.get("source") or {}
    readings = " ".join(
        part
        for part in (
            f"кун {source.get('kun_reading_kana')}"
            if source.get("kun_reading_kana")
            else "",
            f"он {source.get('on_reading_kana')}" if source.get("on_reading_kana") else "",
        )
        if part
    )

    lines.append("")
    lines.append("─" * 64)
    lines.append(f"  {entry['character']}    №{entry['order_index']}    {readings}")
    lines.append("")
    for meaning in entry.get("meanings") or []:
        mark = " " if meaning.get("kind") == "primary" else "·"
        lines.append(f"   {mark} {meaning['en']:<34} {meaning['ru']}")
    lines.append("")
    lines.append("   · — специальное значение (счётный суффикс, зодиак, ключ)")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--from", dest="start", type=int, default=0, help="начать с order_index"
    )
    args = parser.parse_args()

    draft = load_rows(DRAFT_FILE)
    if not draft:
        print(
            f"Черновик {DRAFT_FILE.name} пуст или отсутствует. Сначала:\n"
            "  python -m scripts.etl.translate_meanings --limit 30",
            file=sys.stderr,
        )
        raise SystemExit(1)

    reviewed = {row["character"] for row in load_rows(OVERRIDES_FILE) if row.get("meaning")}

    queue = [
        entry
        for entry in sorted(draft, key=lambda r: r["order_index"])
        if entry["character"] not in reviewed and entry["order_index"] >= args.start
    ]

    if not queue:
        print("Вычитывать нечего: всё из черновика уже перенесено в kanji_ru.json")
        return

    print(f"В очереди {len(queue)} знаков. {HELP}")

    accepted = edited = skipped = 0
    try:
        for position, entry in enumerate(queue, 1):
            print(format_entry(entry))
            suggested = entry.get("meaning_ru")

            if not suggested:
                # Основных значений нет вовсе — предлагать нечего, только ввод.
                print("\n   основных значений нет, введите своё (пустое — пропуск)")
                value = input(f"   [{position}/{len(queue)}] значение: ").strip()
                if not value:
                    skipped += 1
                    continue
                append_override({"character": entry["character"], "meaning": value})
                accepted += 1
                edited += 1
                continue

            print(f"\n   предлагается: {suggested}")
            answer = input(f"   [{position}/{len(queue)}] [Enter/a] e s q: ").strip().lower()

            if answer == "q":
                break
            if answer == "s":
                skipped += 1
                continue
            if answer == "e":
                value = _input_with_default("   значение: ", suggested).strip()
                if not value:
                    skipped += 1
                    continue
                if value != suggested:
                    edited += 1
            elif answer in ("", "a"):
                value = suggested
            else:
                print(f"   не понял ответ {answer!r} — пропускаю")
                skipped += 1
                continue

            append_override({"character": entry["character"], "meaning": value})
            accepted += 1
    except (KeyboardInterrupt, EOFError):
        print("\n прервано")

    print("")
    print(f"  принято:    {accepted} (из них правлено вручную: {edited})")
    print(f"  пропущено:  {skipped}")
    print(f"  в очереди осталось: {len(queue) - accepted - skipped}")
    if accepted:
        print("")
        print("  Принятые знаки опубликуются после пересборки:")
        print("    python -m scripts.build_dataset")
        print("")
        print("  У них пока нет writing_note и example_words — экран прописи")
        print("  и блок слов-примеров останутся пустыми, пока их не добавить")
        print(f"  вручную в {OVERRIDES_FILE.name}.")


if __name__ == "__main__":
    main()
