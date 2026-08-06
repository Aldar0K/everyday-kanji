from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Device, Kanji, Review
from app.routers.reviews import current_device_id
from app.schemas import StatsOut
from app.services.timezone import local_day_start_utc

router = APIRouter(prefix="/stats", tags=["статистика"])


@router.get("", response_model=StatsOut)
async def stats(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> StatsOut:
    device_id = current_device_id(request)
    now = datetime.now(UTC)

    tz_name = (
        await session.scalar(select(Device.timezone).where(Device.id == device_id))
        or "UTC"
    )
    day_start = local_day_start_utc(tz_name, now)

    total_studied = await session.scalar(
        select(func.count()).select_from(Review).where(Review.device_id == device_id)
    )
    due_now = await session.scalar(
        select(func.count())
        .select_from(Review)
        .where(Review.device_id == device_id, Review.next_review_at <= now)
    )
    # Считает карточки, затронутые сегодня, а не общее число ответов:
    # last_reviewed_at хранит только последний ответ. Для честной истории
    # понадобился бы отдельный журнал, но геймификации в приложении нет.
    reviewed_today = await session.scalar(
        select(func.count())
        .select_from(Review)
        .where(Review.device_id == device_id, Review.last_reviewed_at >= day_start)
    )
    published_total = await session.scalar(
        select(func.count()).select_from(Kanji).where(Kanji.is_published.is_(True))
    )

    return StatsOut(
        total_studied=total_studied or 0,
        due_now=due_now or 0,
        reviewed_today=reviewed_today or 0,
        published_total=published_total or 0,
        timezone=tz_name,
    )
