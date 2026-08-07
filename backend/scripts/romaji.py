"""Транслитерация каны в латиницу для чтений кандзи.

Зачем свой модуль, а не pykakasi: на входе уже чистая кана, то есть нужна
транслитерация по таблице из ~110 слогов, а не конвертация кандзи→кана, ради
которой существует pykakasi. Плюс нотацию KANJIDIC (точка перед окуриганой,
дефис у префиксов) всё равно пришлось бы разбирать самому, а система записи
долгот у pykakasi по умолчанию другая — см. ниже.

СИСТЕМА ЗАПИСИ. Повторяет конвенцию, уже сложившуюся в data/kanji_ru.json на
81 вычитанной вручную записи. Это не выбор из вкусовых соображений: половина
поля заполнена руками, и смешивать в одном столбце две системы хуже, чем
последовательно держаться одной, пусть и не самой академичной.

1. Долгие гласные пишутся так, как записаны каной: ジュウ → juu, ジョウ → jou,
   チュウ → chuu, とお → too. Не juu → jū: макронов в существующих записях нет,
   и на телефоне их не набрать.

2. ん всегда n, даже перед губными: しんぶん → shinbun, а не shimbun.

   Классический Хэпбёрн требует здесь m. Не берём по трём причинам. Во-первых,
   правило m идёт в комплекте с макронами, а макроны мы уже отвергли в п. 1:
   взять из системы одно правило и отбросить другое — значит получить гибрид,
   не совпадающий ни с одной реальной системой записи. Во-вторых, аудитория
   приложения — новички, не знающие каны, для которых ромадзи это подсказка к
   произношению и то, что набирают на клавиатуре: shinbun даёт しんぶん,
   shimbun даёт しむぶん. В-третьих, одно правило без исключений проще
   удержать в голове, чем правило со списком губных.

   Перед гласной и перед y ставится апостроф: しんあい → shin'ai. Здесь он не
   косметический — без него запись совпала бы с しない (shinai), то есть
   чтение стало бы читаться неоднозначно.

3. Сокуон っ удваивает следующую согласную: みっつ → mittsu. Единственное
   исключение — перед ch пишется tch (まっちゃ → matcha), потому что cch не
   используется ни в одной системе и выглядит опечаткой.

4. ぢ/づ записываются как ji/zu — совпадают по звучанию с じ/ず.

НОТАЦИЯ KANJIDIC. В кун-чтениях точка отделяет часть, записываемую кандзи, от
окуриганы, а дефис помечает префикс или суффикс:

    で.る   → de(ru)
    なが.い → naga(i)
    ひと-   → hito
    -がわ   → gawa
"""

from __future__ import annotations

# Диграфы идут первыми: разбор жадный, иначе きゃ распалось бы на ki + ya.
_DIGRAPHS = {
    "きゃ": "kya", "きゅ": "kyu", "きょ": "kyo",
    "しゃ": "sha", "しゅ": "shu", "しょ": "sho",
    "ちゃ": "cha", "ちゅ": "chu", "ちょ": "cho",
    "にゃ": "nya", "にゅ": "nyu", "にょ": "nyo",
    "ひゃ": "hya", "ひゅ": "hyu", "ひょ": "hyo",
    "みゃ": "mya", "みゅ": "myu", "みょ": "myo",
    "りゃ": "rya", "りゅ": "ryu", "りょ": "ryo",
    "ぎゃ": "gya", "ぎゅ": "gyu", "ぎょ": "gyo",
    "じゃ": "ja", "じゅ": "ju", "じょ": "jo",
    "ぢゃ": "ja", "ぢゅ": "ju", "ぢょ": "jo",
    "びゃ": "bya", "びゅ": "byu", "びょ": "byo",
    "ぴゃ": "pya", "ぴゅ": "pyu", "ぴょ": "pyo",
    # Изредка встречаются в заимствованных чтениях.
    "ふぁ": "fa", "ふぃ": "fi", "ふぇ": "fe", "ふぉ": "fo",
    "うぃ": "wi", "うぇ": "we", "てぃ": "ti", "でぃ": "di",
    "ゔぁ": "va", "ゔぃ": "vi", "ゔぇ": "ve", "ゔぉ": "vo",
}

_SINGLES = {
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "ざ": "za", "じ": "ji", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    "だ": "da", "ぢ": "ji", "づ": "zu", "で": "de", "ど": "do",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "ゐ": "wi", "ゑ": "we", "を": "o",
    "ゔ": "vu",
    # Мелкие каны вне диграфа: встречаются в записи вроде ぁ после согласной.
    "ぁ": "a", "ぃ": "i", "ぅ": "u", "ぇ": "e", "ぉ": "o",
    "ゃ": "ya", "ゅ": "yu", "ょ": "yo",
}

_SOKUON = "っ"
_N = "ん"
_LONG_MARK = "ー"

# Катакана и хирагана отличаются ровно на этот сдвиг в таблице Unicode, так
# что отдельная таблица для катаканы не нужна.
_KATAKANA_SHIFT = ord("ア") - ord("あ")

_VOWELS = frozenset("aiueo")


def _to_hiragana(text: str) -> str:
    out = []
    for ch in text:
        if "ァ" <= ch <= "ヶ":
            out.append(chr(ord(ch) - _KATAKANA_SHIFT))
        else:
            out.append(ch)
    return "".join(out)


def kana_to_romaji(kana: str) -> str:
    """Транслитерирует строку каны. Незнакомые символы пропускаются."""
    text = _to_hiragana(kana.strip())
    out: list[str] = []
    i = 0
    pending_sokuon = False

    while i < len(text):
        ch = text[i]

        if ch == _SOKUON:
            pending_sokuon = True
            i += 1
            continue

        if ch == _LONG_MARK:
            # Знак долготы повторяет предыдущую гласную: コーヒー → koohii.
            if out and out[-1] and out[-1][-1] in _VOWELS:
                out.append(out[-1][-1])
            i += 1
            continue

        if ch == _N:
            # Апостроф нужен только там, где иначе n слилось бы со следующим
            # слогом в другое чтение: しんあい shin'ai против しない shinai.
            nxt = text[i + 1] if i + 1 < len(text) else ""
            follower = _DIGRAPHS.get(text[i + 1 : i + 3]) or _SINGLES.get(nxt, "")
            out.append("n'" if follower and follower[0] in "aiueoy" else "n")
            i += 1
            continue

        pair = text[i : i + 2]
        syllable = _DIGRAPHS.get(pair)
        if syllable is not None:
            i += 2
        else:
            syllable = _SINGLES.get(ch)
            i += 1
            if syllable is None:
                # Не кана — отдаём как есть, чтобы не терять символ молча.
                if ch.strip():
                    out.append(ch)
                pending_sokuon = False
                continue

        if pending_sokuon:
            # cch не используется ни в одной системе записи, поэтому っ+ch
            # даёт tch: まっちゃ → matcha.
            syllable = ("t" if syllable.startswith("ch") else syllable[0]) + syllable
            pending_sokuon = False

        out.append(syllable)

    return "".join(out)


def reading_to_romaji(reading: str | None) -> str | None:
    """Переводит чтение в нотации KANJIDIC2 в ромадзи.

    Точка отделяет окуригану — она уходит в скобки; дефисы, помечающие
    префикс и суффикс, отбрасываются.

        で.る   → de(ru)
        なが.い → naga(i)
        ひと-   → hito
        サン    → san
    """
    if not reading:
        return None

    cleaned = reading.strip().strip("-")
    if not cleaned:
        return None

    stem, _, okurigana = cleaned.partition(".")

    # KANJIDIC ставит сокуон в конец основы: みっ.つ. Звучит это как mittsu,
    # то есть っ удваивает первую согласную ОКУРИГАНЫ, а не основы. Оставь мы
    # его в основе — удваивать было бы нечего, и гемината потерялась бы
    # («mi(tsu)» вместо «mi(ttsu)»). Поэтому переносим っ через границу.
    if okurigana and stem.endswith(_SOKUON):
        stem, okurigana = stem[:-1], _SOKUON + okurigana

    stem_romaji = kana_to_romaji(stem)
    if not stem_romaji:
        return None

    if not okurigana:
        return stem_romaji

    okurigana_romaji = kana_to_romaji(okurigana.strip("-"))
    if not okurigana_romaji:
        return stem_romaji
    return f"{stem_romaji}({okurigana_romaji})"
