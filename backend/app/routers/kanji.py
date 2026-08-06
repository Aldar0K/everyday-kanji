from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Kanji
from app.schemas import KanjiListOut, KanjiOut
from app.services import cache

router = APIRouter(prefix="/kanji", tags=["справочник"])

MAX_LIMIT = 100


@router.get("", response_model=KanjiListOut)
async def list_kanji(
    session: AsyncSession = Depends(get_session),
    limit: int = Query(20, ge=1, le=MAX_LIMIT),
    offset: int = Query(0, ge=0),
    jlpt: str | None = Query(None, pattern="^N[1-5]$"),
) -> KanjiListOut:
    """Справочник с пагинацией и фильтром по уровню JLPT.

    Отдаются только опубликованные записи: у неопубликованных нет выверенного
    русского значения, показывать их пользователю нельзя.
    """
    cache_key = f"list:{limit}:{offset}:{jlpt or 'all'}"
    if (cached := await cache.get_json(cache_key)) is not None:
        return KanjiListOut(**cached)

    conditions = [Kanji.is_published.is_(True)]
    if jlpt:
        conditions.append(Kanji.jlpt_level == jlpt)

    total = await session.scalar(
        select(func.count()).select_from(Kanji).where(*conditions)
    )
    rows = await session.scalars(
        select(Kanji)
        .where(*conditions)
        .order_by(Kanji.order_index)
        .limit(limit)
        .offset(offset)
    )

    payload = KanjiListOut(
        items=[KanjiOut.model_validate(row) for row in rows],
        total=total or 0,
        limit=limit,
        offset=offset,
    )
    await cache.set_json(cache_key, payload.model_dump(mode="json"))
    return payload


@router.get("/{kanji_id}", response_model=KanjiOut)
async def get_kanji(
    kanji_id: int,
    session: AsyncSession = Depends(get_session),
) -> KanjiOut:
    kanji = await session.get(Kanji, kanji_id)
    if kanji is None or not kanji.is_published:
        raise HTTPException(status_code=404, detail="Кандзи не найден")
    return KanjiOut.model_validate(kanji)
