from fastapi import APIRouter

from app.schemas import SourceOut, SourcesOut
from app.sources import SCREEN_ATTRIBUTION_REQUIRED, SOURCES

router = APIRouter(prefix="/sources", tags=["источники"])


@router.get("", response_model=SourcesOut)
async def list_sources() -> SourcesOut:
    """Источники данных справочника, их авторы, лицензии и внесённые изменения.

    Эндпоинт статический и намеренно не ходит в базу: это метаданные проекта,
    а не пользовательские данные. Нужен, чтобы интерфейс мог показать
    указание авторства — CC BY-SA у KANJIDIC2 и KanjiVG требует именно
    экранного упоминания, а не только строчки в репозитории.
    """
    return SourcesOut(
        sources=[SourceOut(**source) for source in SOURCES],
        screen_attribution_required=list(SCREEN_ATTRIBUTION_REQUIRED),
    )
