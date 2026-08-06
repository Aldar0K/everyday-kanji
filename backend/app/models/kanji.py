from datetime import datetime

from sqlalchemy import Boolean, DateTime, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Kanji(Base):
    """Справочник иероглифов — данные общие для всех устройств."""

    __tablename__ = "kanji"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    character: Mapped[str] = mapped_column(String(4), unique=True, nullable=False)

    # Позиция в курсе. Раньше во фронтенде это был «день N» от общей даты
    # старта, то есть все пользователи шли синхронно. С появлением SRS каждый
    # идёт своим темпом, поэтому порядок стал свойством справочника, а не
    # календаря.
    order_index: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)

    # Выверенное человеком значение. Только оно показывается пользователю.
    meaning: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Догадка автоматического вывода. Хранится отдельно и наружу не отдаётся:
    # замеры показали, что она ошибается примерно на каждом пятом базовом
    # кандзи (山 → «спекуляция», 子 → «крыса»). Нужна только как черновик для
    # ручной вычитки.
    meaning_suggested: Mapped[str | None] = mapped_column(Text, nullable=True)
    meaning_en: Mapped[str | None] = mapped_column(Text, nullable=True)

    kun_reading_kana: Mapped[str | None] = mapped_column(String(64), nullable=True)
    kun_reading_romaji: Mapped[str | None] = mapped_column(String(64), nullable=True)
    on_reading_kana: Mapped[str | None] = mapped_column(String(64), nullable=True)
    on_reading_romaji: Mapped[str | None] = mapped_column(String(64), nullable=True)

    jlpt_level: Mapped[str | None] = mapped_column(String(2), nullable=True)
    stroke_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    frequency: Mapped[int | None] = mapped_column(Integer, nullable=True)
    radical_number: Mapped[int | None] = mapped_column(Integer, nullable=True)

    writing_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Упорядоченные массивы, которые всегда читаются целиком вместе с кандзи и
    # никогда не запрашиваются по отдельности. Нормализация дала бы два JOIN-а
    # ради нулевого выигрыша; при необходимости выносится миграцией.
    example_words: Mapped[list] = mapped_column(
        JSONB, nullable=False, server_default="[]"
    )
    strokes: Mapped[list] = mapped_column(JSONB, nullable=False, server_default="[]")

    # В уроки попадают только записи с выверенным русским текстом. Флаг не даёт
    # показать экран урока с пустым значением: справочные данные у нас есть на
    # все 2136 кандзи, а готовый к обучению контент — не на все.
    is_published: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )
    needs_review: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        # Основная выборка курса: опубликованные, по порядку.
        Index("ix_kanji_published_order", "is_published", "order_index"),
        Index("ix_kanji_jlpt_level", "jlpt_level"),
    )
