"""Расчёт интервалов по алгоритму SM-2.

Отличия от канонического SM-2 и почему они сделаны:

1. Оценок три, а не шесть. Классические 0–5 — слишком богатый выбор для
   человека, который ещё не знает каны, и это противоречит спокойному тону
   приложения. Кнопки отображаются в q следующим образом:
       «не помню» → 2, «помню» → 4, «легко» → 5.

2. Полноценных learning steps (1 мин → 10 мин, как в Anki) нет: они требуют
   отдельной машины состояний. Вместо этого при ответе «не помню» карточка
   возвращается через 10 минут.

   Следствие: interval_days и next_review_at могут расходиться. Первое хранит
   интервал по SM-2 в днях (при провале — 0), второе — фактический момент
   следующего показа. Это осознанное упрощение, а не рассинхрон.
"""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from app.schemas.review import Grade

# Оценки в терминах SM-2.
_QUALITY: dict[Grade, int] = {
    Grade.AGAIN: 2,
    Grade.GOOD: 4,
    Grade.EASY: 5,
}

# Ниже этого значения коэффициент лёгкости не опускается — иначе карточка
# застрянет на минимальных интервалах навсегда.
MIN_EASE_FACTOR = Decimal("1.30")
DEFAULT_EASE_FACTOR = Decimal("2.50")

# Через сколько показать карточку снова после «не помню».
LAPSE_DELAY = timedelta(minutes=10)


@dataclass(frozen=True)
class SrsState:
    repetitions: int
    interval_days: int
    ease_factor: Decimal
    next_review_at: datetime
    is_lapse: bool


def compute_next(
    *,
    grade: Grade,
    repetitions: int,
    interval_days: int,
    ease_factor: Decimal,
    now: datetime | None = None,
) -> SrsState:
    """Считает новое состояние карточки после ответа."""
    now = now or datetime.now(UTC)
    quality = _QUALITY[grade]

    new_ease = _update_ease(ease_factor, quality)

    # q < 3 — ответ провален: прогрессия сбрасывается.
    if quality < 3:
        return SrsState(
            repetitions=0,
            interval_days=0,
            ease_factor=new_ease,
            next_review_at=now + LAPSE_DELAY,
            is_lapse=True,
        )

    if repetitions == 0:
        new_interval = 1
    elif repetitions == 1:
        new_interval = 6
    else:
        new_interval = max(1, round(interval_days * float(new_ease)))

    return SrsState(
        repetitions=repetitions + 1,
        interval_days=new_interval,
        ease_factor=new_ease,
        next_review_at=now + timedelta(days=new_interval),
        is_lapse=False,
    )


def _update_ease(ease_factor: Decimal, quality: int) -> Decimal:
    """EF' = EF + (0.1 − (5−q)·(0.08 + (5−q)·0.02)), не ниже нижней границы."""
    q = Decimal(quality)
    five = Decimal(5)
    delta = Decimal("0.1") - (five - q) * (
        Decimal("0.08") + (five - q) * Decimal("0.02")
    )
    updated = (ease_factor + delta).quantize(Decimal("0.01"))
    return max(MIN_EASE_FACTOR, updated)
