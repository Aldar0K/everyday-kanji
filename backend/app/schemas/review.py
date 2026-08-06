from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

from app.schemas.kanji import KanjiOut


class Grade(str, Enum):
    """Оценка ответа.

    Канонический SM-2 требует оценку 0–5, но шесть вариантов выбора — слишком
    много для новичка и противоречит спокойному тону приложения. Три кнопки
    отображаются во внутренние значения q при расчёте.
    """

    AGAIN = "again"  # не помню
    GOOD = "good"  # помню
    EASY = "easy"  # легко


class ReviewSubmitIn(BaseModel):
    grade: Grade


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    kanji_id: int
    repetitions: int
    interval_days: int
    ease_factor: float
    next_review_at: datetime
    last_reviewed_at: datetime | None
    lapses: int
    total_reviews: int


class LessonTodayOut(BaseModel):
    """Материал на сегодня: что повторить и какой знак изучить новым."""

    due: list[KanjiOut]
    new_kanji: KanjiOut | None
    # Сколько знаков начато сегодня — считается по локальным суткам устройства.
    new_introduced_today: int


class StatsOut(BaseModel):
    total_studied: int
    due_now: int
    reviewed_today: int
    published_total: int
    timezone: str
