"""Источники данных справочника и их лицензии.

Единственное место, где этот список описан. Из него собирается и ответ
GET /api/sources, и корневой ATTRIBUTION.md (scripts/render_attribution.py) —
чтобы файл в репозитории и то, что видит пользователь, не могли разъехаться.

Про лицензии здесь важно не «поставить галочку»: KANJIDIC2 и KanjiVG
распространяются под CC BY-SA, и обе требуют указания авторства. Лицензия
EDRDG отдельно оговаривает, что для веб-приложений, показывающих словарные
данные, упоминание источника должно быть доступно с экрана — см. пометку
у соответствующей записи.
"""

from __future__ import annotations

from typing import TypedDict


class Source(TypedDict):
    id: str
    title: str
    url: str
    authors: str
    license: str
    license_url: str
    provides: str
    version: str | None
    modifications: list[str]


SOURCES: list[Source] = [
    {
        "id": "kanjidic2",
        "title": "KANJIDIC2",
        "url": "https://www.edrdg.org/wiki/index.php/KANJIDIC_Project",
        "authors": (
            "Electronic Dictionary Research and Development Group (EDRDG), "
            "James William Breen и участники проекта"
        ),
        "license": "CC BY-SA 4.0",
        "license_url": "https://www.edrdg.org/edrdg/licence.html",
        "provides": "чтения он и кун, английские значения",
        # Файл на edrdg.org обновляется на месте, отдельных версий у него нет.
        "version": None,
        "modifications": [
            "английские значения переведены на русский моделью Claude "
            "и вычитаны человеком; в уроки попадают только вычитанные",
            "из списка чтений берётся одно, показываемое в карточке; "
            "латиница получена транслитерацией каны",
        ],
    },
    {
        "id": "kanjivg",
        "title": "KanjiVG",
        "url": "https://kanjivg.tagaini.net/",
        "authors": "Ulrich Apel",
        "license": "CC BY-SA 3.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/3.0/",
        "provides": "порядок и траектории черт",
        "version": "r20250816",
        "modifications": [
            "координаты пересчитаны из сетки 109×109 в 0..100 "
            "под систему координат приложения",
        ],
    },
    {
        "id": "jlpt-kanji-dictionary",
        "title": "jlpt-kanji-dictionary",
        "url": "https://github.com/AnchorI/jlpt-kanji-dictionary",
        "authors": "Egor Kiselev",
        "license": "MIT",
        "license_url": (
            "https://github.com/AnchorI/jlpt-kanji-dictionary/blob/main/LICENSE"
        ),
        "provides": "уровни JLPT, частотность, номера ключей, число черт",
        "version": None,
        "modifications": [
            "файл jlpt-kanji.json включён в репозиторий как есть, "
            "вместе с текстом лицензии",
            "частотность используется как порядок изучения: "
            "чем употребительнее знак, тем раньше он в курсе",
        ],
    },
]

# Лицензия EDRDG требует, чтобы веб-приложение, показывающее словарные данные,
# указывало источник на экране, а не только в документации. Пока в интерфейсе
# такого экрана нет — этот эндпоинт существует, чтобы его можно было собрать
# без обращения к бэкенду за данными.
SCREEN_ATTRIBUTION_REQUIRED = ("kanjidic2", "kanjivg")
