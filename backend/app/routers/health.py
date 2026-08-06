from fastapi import APIRouter

router = APIRouter(tags=["служебное"])


@router.get("/health")
async def health() -> dict[str, str]:
    """Проверка живости процесса.

    Намеренно не трогает базу и Redis: это liveness-проба, она должна отвечать
    даже когда зависимости лежат, иначе оркестратор начнёт перезапускать
    исправное приложение. Проверка готовности зависимостей — отдельная задача.
    """
    return {"status": "ok"}
