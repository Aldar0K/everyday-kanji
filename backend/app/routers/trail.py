from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Device, Kanji, Review
from app.routers.reviews import current_device_id
from app.schemas import TrailNodeOut, TrailOut
from app.schemas.kanji import KanjiOut
from app.services.timezone import local_day_start_utc

router = APIRouter(prefix="/trail", tags=["тропа"])


@router.get("", response_model=TrailOut)
async def trail(
    request: Request,
    session: AsyncSession = Depends(get_session),
    recent: int = Query(3, ge=0, le=10),
) -> TrailOut:
    """Данные главного экрана.

    Номер знака («день 9») — это порядок изучения именно этим устройством, а
    не общий календарный день курса: с появлением SRS каждый идёт своим
    темпом, и глобальная дата старта потеряла смысл.

    Позиции не считаются оконной функцией: достаточно знать общее число
    изученных, тогда у i-го с конца позиция равна studied_count - i. Так
    выборка остаётся короткой независимо от того, сколько знаков пройдено.
    """
    device_id = current_device_id(request)
    now = datetime.now(UTC)

    tz_name = (
        await session.scalar(select(Device.timezone).where(Device.id == device_id))
        or "UTC"
    )
    day_start = local_day_start_utc(tz_name, now)

    studied_count = (
        await session.scalar(
            select(func.count()).select_from(Review).where(Review.device_id == device_id)
        )
        or 0
    )

    # Последние изученные, от новых к старым. Берём на один больше, чем нужно
    # для ленты: самый свежий может оказаться знаком сегодняшнего дня.
    rows = (
        await session.execute(
            select(Kanji, Review.created_at, Review.next_review_at)
            .join(Review, Review.kanji_id == Kanji.id)
            .where(Review.device_id == device_id)
            .order_by(Review.created_at.desc())
            .limit(recent + 1)
        )
    ).all()

    def node(index: int) -> TrailNodeOut:
        """index — расстояние от самого свежего знака."""
        kanji_obj = rows[index][0]
        return TrailNodeOut(
            kanji=KanjiOut.model_validate(kanji_obj),
            position=studied_count - index,
        )

    today_node: TrailNodeOut | None = None
    today_completed = False
    recent_start = 0

    if rows and rows[0][1] >= day_start:
        # Сегодня уже начали знак — он и есть знак дня.
        today_node = node(0)
        next_review_at = rows[0][2]
        # Урок пройден, если карточка уехала за пределы текущего момента.
        today_completed = bool(next_review_at and next_review_at > now)
        recent_start = 1
    else:
        started = select(Review.kanji_id).where(Review.device_id == device_id)
        next_kanji = await session.scalar(
            select(Kanji)
            .where(Kanji.is_published.is_(True), Kanji.id.notin_(started))
            .order_by(Kanji.order_index)
            .limit(1)
        )
        if next_kanji is not None:
            today_node = TrailNodeOut(
                kanji=KanjiOut.model_validate(next_kanji), position=studied_count + 1
            )

    # Тропа рисуется сверху вниз от старых к новым, поэтому разворачиваем.
    recent_nodes = [node(i) for i in range(recent_start, len(rows))][:recent]
    recent_nodes.reverse()

    due_count = (
        await session.scalar(
            select(func.count())
            .select_from(Review)
            .where(Review.device_id == device_id, Review.next_review_at <= now)
        )
        or 0
    )
    published_total = (
        await session.scalar(
            select(func.count()).select_from(Kanji).where(Kanji.is_published.is_(True))
        )
        or 0
    )

    return TrailOut(
        studied_count=studied_count,
        recent=recent_nodes,
        today=today_node,
        today_completed=today_completed,
        due_count=due_count,
        published_total=published_total,
        timezone=tz_name,
    )
