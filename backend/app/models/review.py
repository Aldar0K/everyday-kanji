import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Review(Base):
    """Прогресс устройства по конкретному кандзи (состояние SM-2)."""

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False,
    )
    kanji_id: Mapped[int] = mapped_column(
        ForeignKey("kanji.id", ondelete="CASCADE"), nullable=False
    )

    # У всех счётчиков задан и default, и server_default. server_default
    # действует только на уровне базы, поэтому у ещё не сохранённого объекта
    # поле осталось бы None — и первое же `+= 1` падало бы с TypeError.
    repetitions: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    interval_days: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    # Numeric, а не float: коэффициент читается людьми и сравнивается,
    # двоичный дрейф здесь ни к чему.
    ease_factor: Mapped[Decimal] = mapped_column(
        Numeric(4, 2),
        nullable=False,
        default=Decimal("2.50"),
        server_default="2.50",
    )

    next_review_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    last_reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # Момент знакомства со знаком — отдельно от последнего ответа. Нужен, чтобы
    # ограничивать выдачу новых кандзи одним за локальные сутки.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    lapses: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    total_reviews: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )

    __table_args__ = (
        UniqueConstraint("device_id", "kanji_id", name="uq_reviews_device_kanji"),
        # Основной запрос приложения: что пора повторить этому устройству.
        Index("ix_reviews_device_next_review", "device_id", "next_review_at"),
        # Для подсчёта «сколько знаков начато сегодня».
        Index("ix_reviews_device_created", "device_id", "created_at"),
    )
