"""Сборка справочника кандзи в backend/data/kanji.json.

Запускается вручную и вне рантайма приложения — результат коммитится в
репозиторий, чтобы наполнение базы было воспроизводимым и ревьюилось в PR.

Источники и что берём из каждого:

* KANJIDIC2 (edrdg.org) — чтения он/кун, каноническое английское значение.
  Покрывает все 2136 без пропусков.
* jlpt-kanji.json — уровень JLPT, частотность, радикал, число черт. Лежит
  в data/vendor/, а не качается: репозиторий-источник личный, и его
  исчезновение не должно ломать сборку. Лицензия MIT, рядом файл LICENSE.
* KanjiVG — пути черт, одним релизным XML вместо 2136 запросов к GitHub.
* data/kanji_ru.json — ручная вычитка. Единственный источник поля meaning.
* data/kanji_ru_draft.json — машинный перевод английских глосс, черновик.

ЧТО ПУБЛИКУЕТСЯ. Только записи с выверенным человеком значением: meaning
берётся исключительно из kanji_ru.json, is_published = bool(meaning). Машинный
перевод кладётся в отдельное поле meaning_suggested_ru, наружу не отдаётся и
на публикацию не влияет — он существует ровно как заготовка для вычитки.

Предыдущая версия скрипта пыталась вывести значение косвенно, из словарных
статей, где иероглиф выступает самостоятельным словом. Этот путь закрыт: на
четырнадцати базовых кандзи он давал три грубые ошибки (山 → «спекуляция;
риск», 子 → «крыса, знак зодиака», 本 → «счётный суффикс»). Для обучающего
контента это худший вид ошибки — правдоподобная и ложная. Вместе с выводом
ушла и зависимость от словаря слов на 56 МБ.
"""

from __future__ import annotations

import gzip
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.romaji import reading_to_romaji

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
VENDOR_DIR = DATA_DIR / "vendor"
OUT_FILE = DATA_DIR / "kanji.json"
# Ручная вычитка: только отсюда берутся значения, попадающие в уроки.
OVERRIDES_FILE = DATA_DIR / "kanji_ru.json"
# Машинный черновик: заготовка для вычитки, в meaning не попадает никогда.
DRAFT_FILE = DATA_DIR / "kanji_ru_draft.json"

KANJIDIC_URL = "http://www.edrdg.org/kanjidic/kanjidic2.xml.gz"

# Версия зафиксирована: KanjiVG правит пути между релизами, и незакреплённая
# ссылка означала бы, что пересборка через полгода молча меняет прописи у уже
# опубликованных знаков.
KANJIVG_RELEASE = "r20250816"
KANJIVG_URL = (
    f"https://github.com/KanjiVG/kanjivg/releases/download/{KANJIVG_RELEASE}"
    f"/kanjivg-{KANJIVG_RELEASE.lstrip('r')}.xml.gz"
)

# KanjiVG рисует в сетке 109×109, приложение — в 0..100.
KANJIVG_SCALE = 100.0 / 109.0


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def download(url: str, dest: Path) -> Path:
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    log(f"скачиваю {url}")
    urllib.request.urlretrieve(url, dest)  # noqa: S310
    return dest


# --------------------------------------------------------------------------
# Источники
# --------------------------------------------------------------------------


def load_kanjidic() -> dict[str, dict]:
    """Чтения и английские значения. Глоссы — списком, а не строкой.

    Склеивать их в строку здесь нельзя: у 代 есть глосса «counter for decades
    of ages, eras, etc.» с запятыми внутри, и разобрать склейку обратно уже не
    получится. Перевод значений работает именно со списком.
    """
    gz = download(KANJIDIC_URL, RAW_DIR / "kanjidic2.xml.gz")
    with gzip.open(gz, "rb") as fh:
        root = ET.parse(fh).getroot()

    result: dict[str, dict] = {}
    for char in root.findall("character"):
        literal = char.findtext("literal")
        rm = char.find("reading_meaning")
        if literal is None or rm is None:
            continue
        group = rm.find("rmgroup")
        if group is None:
            continue
        result[literal] = {
            "on": [r.text for r in group.findall("reading[@r_type='ja_on']") if r.text],
            "kun": [
                r.text for r in group.findall("reading[@r_type='ja_kun']") if r.text
            ],
            # Значения без m_lang — английские.
            "meaning_en": [
                m.text for m in group.findall("meaning") if m.get("m_lang") is None
            ],
        }
    return result


def load_jlpt_list() -> list[dict]:
    path = VENDOR_DIR / "jlpt-kanji.json"
    if not path.exists():
        log(f"ОШИБКА: нет {path} — он должен лежать в репозитории")
        raise SystemExit(1)
    return json.loads(path.read_text(encoding="utf-8"))


def load_all_strokes() -> dict[str, list[dict]]:
    """Пути черт для всех знаков разом, из одного релизного XML.

    Раньше качался отдельный SVG на каждый знак, и чтобы не делать 2136
    запросов, черты брались только для публикуемых. Побочный эффект был
    неприятный: публикация нового знака требовала пересборки с сетью. Теперь
    один файл на 3,4 МБ покрывает все 2136, и публикация — чисто локальная
    правка kanji_ru.json.
    """
    gz = download(KANJIVG_URL, RAW_DIR / f"kanjivg-{KANJIVG_RELEASE}.xml.gz")
    with gzip.open(gz, "rb") as fh:
        root = ET.parse(fh).getroot()

    result: dict[str, list[dict]] = {}
    for kanji in root:
        kid = kanji.get("id") or ""
        if not kid.startswith("kvg:kanji_"):
            continue
        code = kid[len("kvg:kanji_") :]
        # Варианты начертания помечены суффиксом через дефис — берём основной.
        if "-" in code:
            continue
        try:
            character = chr(int(code, 16))
        except ValueError:
            continue

        strokes: list[dict] = []
        for path in kanji.iter("path"):
            d = path.get("d")
            if not d:
                continue
            scaled = _scale_path(d)
            start = _start_point(scaled)
            if start is None:
                continue
            strokes.append({"d": scaled, "start": start, "instruction": None})
        if strokes:
            result[character] = strokes
    return result


def _scale_path(d: str) -> str:
    def repl(m: re.Match[str]) -> str:
        value = float(m.group(0)) * KANJIVG_SCALE
        return f"{value:.2f}".rstrip("0").rstrip(".")

    return re.sub(r"-?\d+\.?\d*", repl, d)


def _start_point(d: str) -> dict | None:
    m = re.match(r"M\s*(-?\d+\.?\d*)[ ,](-?\d+\.?\d*)", d)
    if not m:
        return None
    return {"x": round(float(m.group(1)), 1), "y": round(float(m.group(2)), 1)}


# --------------------------------------------------------------------------
# Чтения
# --------------------------------------------------------------------------


def resolve_reading(
    manual: dict, kanjidic_readings: list[str], kind: str, character: str
) -> tuple[str | None, str | None]:
    """Возвращает пару (кана, ромадзи) для одного вида чтения.

    Кана берётся из вычитки, если там есть, иначе первая из KANJIDIC. Ромадзи
    считается ИЗ ЭТОЙ ЖЕ каны, поэтому пара не может разойтись по построению.

    Расхождение — не гипотетическая проблема: до появления переопределения
    каны 14 из 160 опубликованных пар противоречили сами себе. У 木 показывался
    ボку с подписью «moku», хотя ボク читается «boku»; человек имел в виду
    モク, но поля для каны в файле вычитки не было. Для приложения, которое
    учит читать кану, это ровно та ошибка, которую нельзя допускать.
    """
    kana_key, romaji_key = f"{kind}_reading_kana", f"{kind}_reading_romaji"

    kana = manual.get(kana_key) or (kanjidic_readings or [None])[0]
    manual_romaji = manual.get(romaji_key)
    derived = reading_to_romaji(kana)

    if manual_romaji and derived and manual_romaji != derived:
        # Человек написал ромадзи, не соответствующий кане, которую мы
        # показываем. Значит, он имел в виду другое чтение — надо дописать
        # кану в kanji_ru.json, а не молча показывать противоречивую пару.
        log(
            f"  ВНИМАНИЕ {character} {kind}: кана {kana} читается «{derived}», "
            f"а в вычитке «{manual_romaji}». Допишите {kana_key} в kanji_ru.json"
        )

    return kana, manual_romaji or derived


# --------------------------------------------------------------------------
# Сборка
# --------------------------------------------------------------------------


def main() -> None:
    log("читаю KANJIDIC2…")
    kanjidic = load_kanjidic()
    log("читаю список JLPT…")
    jlpt = load_jlpt_list()
    log("читаю пути черт KanjiVG…")
    strokes_by_char = load_all_strokes()
    log(f"  черты есть у {len(strokes_by_char)} знаков")

    overrides = _load_json_by_character(OVERRIDES_FILE)
    log(f"ручная вычитка: {len(overrides)} записей")
    draft = _load_json_by_character(DRAFT_FILE)
    log(f"машинный черновик: {len(draft)} записей")

    result = []
    published = 0
    for position, row in enumerate(
        sorted(jlpt, key=lambda r: r.get("frequency") or 10**6), 1
    ):
        char = row["kanji"]
        kd = kanjidic.get(char, {})
        manual = overrides.get(char) or {}

        # meaning заполняется ТОЛЬКО вычитанным значением. Машинный перевод
        # остаётся отдельным полем и в интерфейс не попадает.
        meaning = manual.get("meaning")
        suggested_ru = (draft.get(char) or {}).get("meaning_ru")

        kun_kana, kun_romaji = resolve_reading(manual, kd.get("kun") or [], "kun", char)
        on_kana, on_romaji = resolve_reading(manual, kd.get("on") or [], "on", char)

        entry = {
            "character": char,
            "order_index": position,
            "meaning": meaning,
            "meaning_suggested_ru": suggested_ru,
            "meaning_en": ", ".join(kd.get("meaning_en") or []) or None,
            "kun_reading_kana": kun_kana,
            "kun_reading_romaji": kun_romaji,
            "on_reading_kana": on_kana,
            "on_reading_romaji": on_romaji,
            "jlpt_level": row.get("jlpt"),
            "stroke_count": row.get("strokes"),
            "frequency": row.get("frequency"),
            "radical_number": row.get("radical_number"),
            "writing_note": manual.get("writing_note"),
            "example_words": manual.get("example_words") or [],
            "strokes": strokes_by_char.get(char, []),
            "is_published": bool(meaning),
            # Есть машинный перевод, но нет вычитки — кандидат в очередь.
            "needs_review": bool(suggested_ru) and not meaning,
        }
        if entry["is_published"]:
            published += 1
        result.append(entry)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log(f"записано {len(result)} кандзи в {OUT_FILE}")
    log(f"опубликовано (вычитано вручную): {published}")
    log(f"есть машинный перевод, ждут вычитки: {sum(r['needs_review'] for r in result)}")
    log(f"без черт: {sum(1 for r in result if not r['strokes'])}")


def _load_json_by_character(path: Path) -> dict[str, dict]:
    if not path.exists():
        log(f"нет {path.name} — пропускаю")
        return {}
    rows = json.loads(path.read_text(encoding="utf-8"))
    return {row["character"]: row for row in rows}


if __name__ == "__main__":
    main()
