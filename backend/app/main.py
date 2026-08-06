import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import redis_client
from app.config import settings
from app.middleware import DeviceMiddleware, RateLimitMiddleware
from app.routers import health, kanji, lesson, reviews, stats

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ANN201, ARG001
    # Миграции здесь намеренно не запускаются: при нескольких воркерах это
    # даёт гонку. Схема накатывается отдельной командой на деплое:
    #   docker compose run --rm backend alembic upgrade head
    if not await redis_client.ping():
        logger.warning(
            "Redis недоступен на старте: лимитер и кэш будут работать вхолостую."
        )
    yield
    await redis_client.close()


app = FastAPI(
    title="Everyday Kanji API",
    lifespan=lifespan,
    # Документацию наружу отдаём только вне production.
    docs_url=None if settings.is_production else "/api/docs",
    openapi_url=None if settings.is_production else "/api/openapi.json",
)

# Порядок важен: middleware выполняются в обратном порядке добавления, поэтому
# лимитер должен стоять раньше работы с устройством — незачем ходить в базу за
# устройством для запроса, который всё равно будет отклонён.
app.add_middleware(DeviceMiddleware)
app.add_middleware(RateLimitMiddleware)

app.include_router(health.router, prefix="/api")
app.include_router(kanji.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")
app.include_router(lesson.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
