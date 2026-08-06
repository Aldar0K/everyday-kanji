import logging

import redis.asyncio as aioredis

from app.config import settings

logger = logging.getLogger(__name__)

# decode_responses=True — работаем со строками, а не с bytes: все значения,
# которые мы кладём в Redis, текстовые (JSON и счётчики).
redis_client: aioredis.Redis = aioredis.from_url(
    settings.redis_url,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)


async def ping() -> bool:
    """Доступен ли Redis. Используется при старте, чтобы предупредить в логах."""
    try:
        return bool(await redis_client.ping())
    except Exception as exc:  # noqa: BLE001 — важен сам факт недоступности
        logger.warning("Redis недоступен: %s", exc)
        return False


async def close() -> None:
    await redis_client.aclose()
