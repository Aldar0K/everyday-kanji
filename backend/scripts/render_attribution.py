"""Генерация корневого ATTRIBUTION.md из app/sources.py.

    python -m scripts.render_attribution          # перезаписать файл
    python -m scripts.render_attribution --check  # только проверить свежесть

Файл генерируется, а не пишется руками, чтобы список источников существовал
ровно в одном месте: иначе ATTRIBUTION.md и ответ GET /api/sources рано или
поздно разойдутся, и разойдутся именно в тексте про лицензии.
"""

from __future__ import annotations

import sys
from pathlib import Path

from app.sources import SCREEN_ATTRIBUTION_REQUIRED, SOURCES

OUT_FILE = Path(__file__).resolve().parent.parent.parent / "ATTRIBUTION.md"

HEADER = """\
# Источники данных

Справочник кандзи собран из открытых источников. Ниже — что взято из каждого,
кто автор, под какой лицензией распространяется и что мы изменили.

Файл сгенерирован из `backend/app/sources.py`; те же данные отдаёт
`GET /api/sources`. Править нужно модуль, а не этот файл.
"""

FOOTER = """\
## Что в проекте своё

* Русские значения иероглифов в уроках — перевод английских глосс KANJIDIC2
  с последующей вычиткой человеком. Значение попадает в приложение только
  после того, как его подтвердил человек; машинный перевод хранится отдельным
  полем и наружу не отдаётся.
* Описания порядка написания (`writing_note`), слова-примеры и их переводы
  написаны вручную.
* Код приложения.

## Производные работы

KANJIDIC2 и KanjiVG распространяются под лицензиями CC BY-SA. Это copyleft:
производные данные должны распространяться на тех же условиях. Собранный
`backend/data/kanji.json` содержит материал обоих источников и потому
наследует CC BY-SA.
"""


def render() -> str:
    parts = [HEADER]

    for source in SOURCES:
        parts.append(f"\n## {source['title']}\n")
        parts.append(f"* Ссылка: {source['url']}")
        parts.append(f"* Авторы: {source['authors']}")
        parts.append(f"* Лицензия: [{source['license']}]({source['license_url']})")
        if source["version"]:
            parts.append(f"* Версия: {source['version']}")
        parts.append(f"* Что взято: {source['provides']}")
        if source["id"] in SCREEN_ATTRIBUTION_REQUIRED:
            parts.append(
                "* Лицензия требует указания источника в интерфейсе приложения, "
                "не только в репозитории"
            )
        parts.append("\nЧто изменено:\n")
        for change in source["modifications"]:
            parts.append(f"* {change}")
        parts.append("")

    parts.append("")
    parts.append(FOOTER)
    return "\n".join(parts)


def main() -> None:
    content = render()
    if "--check" in sys.argv:
        current = OUT_FILE.read_text(encoding="utf-8") if OUT_FILE.exists() else ""
        if current != content:
            print(
                f"{OUT_FILE.name} устарел относительно app/sources.py.\n"
                "Обновите: python -m scripts.render_attribution",
                file=sys.stderr,
            )
            raise SystemExit(1)
        print(f"{OUT_FILE.name} актуален")
        return

    OUT_FILE.write_text(content, encoding="utf-8")
    print(f"записано {OUT_FILE}")


if __name__ == "__main__":
    main()
