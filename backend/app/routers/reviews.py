import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_session
from app.models import Kanji, Review
from app.schemas import KanjiOut, ReviewOut, ReviewSubmitIn
from app.services import srs

router = APIRouter(prefix="/reviews", tags=["повторения"])


def current_device_id(request: Request) -> uuid.UUID:
    device_id = getattr(request.state, "device_id", None)
    if device_id is None:
        # Сюда можно попасть только если middleware не отработал.
        raise HTTPException(status_code=500, detail="Устройство не определено")
    return device_id


@router.get("/due", response_model=list[KanjiOut])
async def due_reviews(
    request: Request,
    session: AsyncSession = Depends(get_session),
    limit: int = 50,
) -> list[KanjiOut]:
    """Карточки, которые пора повторить. Основной запрос приложения."""
    device_id = current_device_id(request)
    rows = await session.scalars(
        select(Kanji)
        .join(Review, Review.kanji_id == Kanji.id)
        .where(
            Review.device_id == device_id,
            Review.next_review_at <= datetime.now(UTC),
            Kanji.is_published.is_(True),
        )
        .order_by(Review.next_review_at)
        .limit(limit)
    )
    return [KanjiOut.model_validate(row) for row in rows]


@router.post("/{kanji_id}", response_model=ReviewOut)
async def submit_review(
    kanji_id: int,
    payload: ReviewSubmitIn,
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> ReviewOut:
    """Приём ответа на карточку и пересчёт SRS."""
    device_id = current_device_id(request)
    now = datetime.now(UTC)

    kanji = await session.get(Kanji, kanji_id)
    if kanji is None or not kanji.is_published:
        raise HTTPException(status_code=404, detail="Кандзи не найден")

    review = await session.scalar(
        select(Review).where(
            Review.device_id == device_id, Review.kanji_id == kanji_id
        )
    )

    if review is None:
        # Все поля задаются явно: default= в модели вычисляется при INSERT, а
        # не при создании объекта, поэтому до сохранения счётчики были бы None
        # и первое же `+= 1` упало бы с TypeError.
        review = Review(
            device_id=device_id,
            kanji_id=kanji_id,
            repetitions=0,
            interval_days=0,
            ease_factor=srs.DEFAULT_EASE_FACTOR,
            next_review_at=now,
            created_at=now,
            lapses=0,
            total_reviews=0,
        )
        session.add(review)
    elif review.last_reviewed_at is not None:
        # Защита от двойного тапа: на мобильном кнопку легко нажать дважды, и
        # без этой проверки интервал продвинулся бы на два шага сразу.
        elapsed = (now - review.last_reviewed_at).total_seconds()
        if elapsed < settings.review_duplicate_window_seconds:
            return ReviewOut.model_validate(review)

    state = srs.compute_next(
        grade=payload.grade,
        repetitions=review.repetitions,
        interval_days=review.interval_days,
        ease_factor=review.ease_factor,
        now=now,
    )

    review.repetitions = state.repetitions
    review.interval_days = state.interval_days
    review.ease_factor = state.ease_factor
    review.next_review_at = state.next_review_at
    review.last_reviewed_at = now
    review.total_reviews += 1
    if state.is_lapse:
        review.lapses += 1

    await session.commit()
    return ReviewOut.model_validate(review)
