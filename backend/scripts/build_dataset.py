"""Сборка справочника кандзи в backend/data/kanji.json.

Запускается вручную и вне рантайма приложения — результат коммитится в
репозиторий, чтобы наполнение базы было воспроизводимым и ревьюилось в PR.

Источники и что берём из каждого:

* KANJIDIC2 (edrdg.org) — чтения он/кун, каноническое английское значение,
  число черт. Покрывает все 2136 без пропусков.
* AnchorI/jlpt-kanji-dictionary, jlpt-kanji.json — уровень JLPT, частотность,
  радикал; ровно 2136 иероглифов дзёё.
* Тот же репозиторий, dictionary_part_*.json — слова с русским переводом.
  Отсюда же выводится русское значение самого кандзи.
* KanjiVG — пути черт.

Про русское значение — здесь главный подвох. Прямого открытого источника
«кандзи → русское значение» не существует, поэтому его приходится выводить из
словарных статей, где иероглиф выступает самостоятельным словом.

Замеры показали, что этому выводу доверять нельзя. Даже с отбором статьи по
совпадению с каноническим значением KANJIDIC получалось: 山 → «спекуляция;
риск» вместо «гора», 子 → «крыса, знак зодиака» вместо «ребёнок», 本 →
«счётный суффикс» вместо «книга». На четырнадцати базовых кандзи три грубо
неверных. Для обучающего контента это худший вид ошибки — правдоподобная и
ложная.

Поэтому автовывод НИЧЕГО не публикует. Он кладёт догадку в meaning_suggested,
а поле meaning заполняется только из файла ручной вычитки data/kanji_ru.json.
is_published=true получают исключительно вычитанные записи. Всё остальное
(чтения, черты, JLPT, частотность) берётся из KANJIDIC2 и KanjiVG и надёжно.
"""

from __future__ import annotations

import gzip
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
OUT_FILE = DATA_DIR / "kanji.json"
# Ручная вычитка: только отсюда берутся значения, попадающие в уроки.
OVERRIDES_FILE = DATA_DIR / "kanji_ru.json"

KANJIDIC_URL = "http://www.edrdg.org/kanjidic/kanjidic2.xml.gz"
REPO_RAW = "https://raw.githubusercontent.com/AnchorI/jlpt-kanji-dictionary/main"
KANJIVG_RAW = "https://raw.githubusercontent.com/KanjiVG/kanjivg/master/kanji"

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
    path = download(f"{REPO_RAW}/jlpt-kanji.json", RAW_DIR / "jlpt-kanji.json")
    return json.loads(path.read_text(encoding="utf-8"))


def load_words() -> list[dict]:
    entries: list[dict] = []
    for part in range(1, 5):
        path = download(
            f"{REPO_RAW}/dictionary_part_{part}.json", RAW_DIR / f"dict_{part}.json"
        )
        entries.extend(json.loads(path.read_text(encoding="utf-8")))
    return entries


def load_strokes(character: str) -> list[dict]:
    """Пути черт из KanjiVG, пересчитанные в систему координат 0..100."""
    code = f"{ord(character):05x}"
    path = RAW_DIR / "kanjivg" / f"{code}.svg"
    try:
        download(f"{KANJIVG_RAW}/{code}.svg", path)
        root = ET.parse(path).getroot()
    except Exception:  # noqa: BLE001 — для части знаков файла может не быть
        return []

    strokes: list[dict] = []
    ns = "{http://www.w3.org/2000/svg}"
    for group in root.iter(f"{ns}g"):
        if not (group.get("id") or "").startswith("kvg:StrokePaths_"):
            continue
        for p in group.iter(f"{ns}path"):
            d = p.get("d")
            if not d:
                continue
            scaled = _scale_path(d)
            start = _start_point(scaled)
            if start is None:
                continue
            strokes.append({"d": scaled, "start": start, "instruction": None})
    return strokes


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
# Вывод русского значения
# --------------------------------------------------------------------------

_WORD_RE = re.compile(r"[a-z]+")


def _tokens(text: str | None) -> set[str]:
    return set(_WORD_RE.findall((text or "").lower()))


def build_single_char_index(words: list[dict], charset: set[str]) -> dict[str, list[dict]]:
    index: dict[str, list[dict]] = {}
    for entry in words:
        word = entry.get("kanji") or ""
        if len(word) == 1 and word in charset and entry.get("glossary_ru"):
            index.setdefault(word, []).append(entry)
    return index


def pick_russian(
    character: str, kanjidic: dict[str, dict], index: dict[str, list[dict]]
) -> tuple[str | None, bool]:
    """Возвращает (русское значение, требуется ли ручная проверка)."""
    candidates = index.get(character)
    if not candidates:
        return None, False

    meanings = kanjidic.get(character, {}).get("meaning_en") or []
    # Первое значение KANJIDIC — основное, поэтому весит больше: иначе для 子
    # («child, sign of the rat») побеждала бы статья про знак зодиака.
    primary = _tokens(meanings[0]) if meanings else set()
    secondary: set[str] = set()
    for m in meanings[1:]:
        secondary |= _tokens(m)

    best, best_score = None, -1
    for entry in candidates:
        english: set[str] = set()
        for gloss in (entry.get("glossary_en") or [])[:6]:
            english |= _tokens(gloss)
        score = 3 * len(english & primary) + len(english & secondary)
        if score > best_score:
            best, best_score = entry, score

    if best is None:
        return None, False

    glosses = best.get("glossary_ru") or []
    if not glosses:
        return None, False

    value = _clean_gloss(glosses[0])
    # Ноль совпадений — статья есть, но смысл не подтвердился.
    return value, best_score == 0


def _clean_gloss(gloss: str) -> str:
    """Убирает нумерацию вида «1) » в начале."""
    return re.sub(r"^\s*\d+\)\s*", "", gloss).strip()


# --------------------------------------------------------------------------
# Сборка
# --------------------------------------------------------------------------


def build_example_words(
    character: str,
    words_by_char: dict[str, list[dict]],
    freq: dict[str, int],
    limit: int = 3,
) -> list[dict]:
    """Слова с этим кандзи, у которых есть русский перевод.

    Данных о частотности слов в источнике нет (поле sequence — это
    идентификатор статьи, а не частота: сортировка по нему давала «山家者» и
    «山蜜» вместо «вулкан»). Поэтому используем косвенный признак: короткие
    слова из частотных кандзи употребительнее длинных из редких.
    """
    candidates = words_by_char.get(character) or []

    def rank(entry: dict) -> tuple:
        word = entry["kanji"]
        # Средняя частотность составляющих иероглифов (меньше — употребительнее).
        ranks = [freq.get(ch, 10**6) for ch in word if ch in freq]
        avg = sum(ranks) / len(ranks) if ranks else 10**6
        unknown = sum(1 for ch in word if ch not in freq and not _is_kana(ch))
        return (len(word), unknown, avg)

    picked = []
    for entry in sorted(candidates, key=rank)[:limit]:
        picked.append(
            {
                "word": entry["kanji"],
                "kana": entry.get("reading"),
                "romaji": None,
                "translation": _clean_gloss((entry.get("glossary_ru") or [""])[0]),
            }
        )
    return picked


def _is_kana(ch: str) -> bool:
    return "぀" <= ch <= "ヿ"


def index_words_by_char(words: list[dict], charset: set[str]) -> dict[str, list[dict]]:
    """Раскладывает слова по каждому входящему в них кандзи — один проход вместо 2136."""
    index: dict[str, list[dict]] = {}
    for entry in words:
        word = entry.get("kanji") or ""
        if len(word) < 2 or not entry.get("glossary_ru"):
            continue
        for ch in set(word):
            if ch in charset:
                index.setdefault(ch, []).append(entry)
    return index


def main() -> None:
    with_strokes = "--with-strokes" in sys.argv

    log("читаю KANJIDIC2…")
    kanjidic = load_kanjidic()
    log("читаю список JLPT…")
    jlpt = load_jlpt_list()
    log("читаю словарь слов…")
    words = load_words()

    charset = {row["kanji"] for row in jlpt}
    single_index = build_single_char_index(words, charset)
    words_by_char = index_words_by_char(words, charset)
    freq = {
        row["kanji"]: row.get("frequency") or 10**6
        for row in jlpt
        if row.get("frequency")
    }

    overrides = _load_overrides()
    log(f"ручная вычитка: {len(overrides)} записей")

    result = []
    published = 0
    for position, row in enumerate(
        sorted(jlpt, key=lambda r: r.get("frequency") or 10**6), 1
    ):
        char = row["kanji"]
        kd = kanjidic.get(char, {})
        suggested, _ = pick_russian(char, kanjidic, single_index)
        manual = overrides.get(char) or {}

        # meaning заполняется ТОЛЬКО вычитанным значением. Догадка автовывода
        # остаётся отдельным полем и в интерфейс не попадает.
        meaning = manual.get("meaning")

        entry = {
            "character": char,
            "order_index": position,
            "meaning": meaning,
            "meaning_suggested": suggested,
            "meaning_en": ", ".join(kd.get("meaning_en") or []) or None,
            "kun_reading_kana": (kd.get("kun") or [None])[0],
            "kun_reading_romaji": manual.get("kun_reading_romaji"),
            "on_reading_kana": (kd.get("on") or [None])[0],
            "on_reading_romaji": manual.get("on_reading_romaji"),
            "jlpt_level": row.get("jlpt"),
            "stroke_count": row.get("strokes"),
            "frequency": row.get("frequency"),
            "radical_number": row.get("radical_number"),
            "writing_note": manual.get("writing_note"),
            "example_words": manual.get("example_words")
            or build_example_words(char, words_by_char, freq),
            # Пути черт качаем только для публикуемых: остальные всё равно не
            # попадут на экран, а это 2136 отдельных запросов к KanjiVG.
            "strokes": load_strokes(char) if (with_strokes and meaning) else [],
            "is_published": bool(meaning),
            # Есть догадка, но нет вычитки — кандидат в очередь на проверку.
            "needs_review": bool(suggested) and not meaning,
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
    log(f"есть догадка, ждут вычитки:       {sum(r['needs_review'] for r in result)}")


def _load_overrides() -> dict[str, dict]:
    if not OVERRIDES_FILE.exists():
        log(f"ВНИМАНИЕ: {OVERRIDES_FILE} не найден — публиковать будет нечего")
        return {}
    rows = json.loads(OVERRIDES_FILE.read_text(encoding="utf-8"))
    return {row["character"]: row for row in rows}


if __name__ == "__main__":
    main()
