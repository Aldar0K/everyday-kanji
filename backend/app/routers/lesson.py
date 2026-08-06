from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Device, Kanji, Review
from app.routers.reviews import current_device_id
from app.schemas import KanjiOut, LessonTodayOut
from app.services.timezone import local_day_start_utc

router = APIRouter(prefix="/lesson", tags=["урок"])

# Сколько новых знаков в сутки. Приложение построено вокруг одного знака в день.
NEW_PER_DAY = 1


@router.get("/today", response_model=LessonTodayOut)
async def lesson_today(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> LessonTodayOut:
    """Материал на сегодня: что повторить и какой знак изучить новым.

    Повторения приходят из SRS, а новый знак — это следующий неначатый кандзи
    по порядку курса. Ограничение «не больше одного в сутки» считается по
    локальным суткам устройства, иначе граница дня уезжала бы относительно
    пользователя.
    """
    device_id = current_device_id(request)
    now = datetime.now(UTC)

    tz_name = await session.scalar(select(Device.timezone).where(Device.id == device_id))
    day_start = local_day_start_utc(tz_name, now)

    due_rows = await session.scalars(
        select(Kanji)
        .join(Review, Review.kanji_id == Kanji.id)
        .where(
            Review.device_id == device_id,
            Review.next_review_at <= now,
            Kanji.is_published.is_(True),
        )
        .order_by(Review.next_review_at)
    )
    due = [KanjiOut.model_validate(row) for row in due_rows]

    introduced_today = (
        await session.scalar(
            select(func.count())
            .select_from(Review)
            .where(Review.device_id == device_id, Review.created_at >= day_start)
        )
        or 0
    )

    new_kanji = None
    if introduced_today < NEW_PER_DAY:
        started = select(Review.kanji_id).where(Review.device_id == device_id)
        new_row = await session.scalar(
            select(Kanji)
            .where(Kanji.is_published.is_(True), Kanji.id.notin_(started))
            .order_by(Kanji.order_index)
            .limit(1)
        )
        if new_row is not None:
            new_kanji = KanjiOut.model_validate(new_row)

    return LessonTodayOut(
        due=due,
        new_kanji=new_kanji,
        new_introduced_today=introduced_today,
    )
