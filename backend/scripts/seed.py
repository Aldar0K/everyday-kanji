"""Наполнение справочника из backend/data/kanji.json.

Запуск:
    docker compose run --rm backend python -m scripts.seed

Наполнение данными намеренно отделено от миграций схемы: это разные по природе
операции с разной частотой запуска.

Ключевое правило: только UPSERT, никаких удалений. У reviews.kanji_id внешний
ключ с ON DELETE CASCADE, поэтому пересоздание строк справочника молча стёрло
бы весь прогресс пользователей.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

from sqlalchemy import func, select, text
from sqlalchemy.dialects.postgresql import insert

from app.database import session_factory
from app.models import Kanji
from app.services import cache

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "kanji.json"

# Поля, которые перезаписываются при повторном запуске.
UPDATABLE = (
    "order_index",
    "meaning",
    "meaning_suggested",
    "meaning_en",
    "kun_reading_kana",
    "kun_reading_romaji",
    "on_reading_kana",
    "on_reading_romaji",
    "jlpt_level",
    "stroke_count",
    "frequency",
    "radical_number",
    "writing_note",
    "example_words",
    "strokes",
    "is_published",
    "needs_review",
)


async def seed() -> None:
    if not DATA_FILE.exists():
        print(
            f"Файл {DATA_FILE} не найден. Сначала соберите справочник:\n"
            "  docker compose run --rm backend python -m scripts.build_dataset",
            file=sys.stderr,
        )
        raise SystemExit(1)

    rows = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    print(f"В файле {len(rows)} записей")

    async with session_factory() as session:
        # order_index уникален, и при переупорядочивании курса обновление по
        # одной строке упёрлось бы в ограничение на полпути. Откладываем
        # проверку до конца транзакции.
        await session.execute(text("SET CONSTRAINTS ALL DEFERRED"))

        # Чтобы не ловить конфликт по order_index между старыми и новыми
        # значениями, сначала уводим существующие индексы в отрицательную
        # область — она заведомо не пересекается с новыми.
        await session.execute(
            text("UPDATE kanji SET order_index = -order_index WHERE order_index > 0")
        )

        for chunk in _chunks(rows, 500):
            stmt = insert(Kanji).values(chunk)
            stmt = stmt.on_conflict_do_update(
                index_elements=[Kanji.character],
                set_={field: getattr(stmt.excluded, field) for field in UPDATABLE},
            )
            await session.execute(stmt)

        await session.commit()

        total = await session.scalar(select(func.count()).select_from(Kanji))
        published = await session.scalar(
            select(func.count()).select_from(Kanji).where(Kanji.is_published.is_(True))
        )

    # Справочник изменился — обесцениваем кэш.
    await cache.bump_version()

    print(f"В базе всего: {total}, опубликовано: {published}")


def _chunks(items: list, size: int):  # noqa: ANN202
    for i in range(0, len(items), size):
        yield items[i : i + size]


if __name__ == "__main__":
    asyncio.run(seed())
