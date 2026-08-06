"""Кэш справочника кандзи.

Справочник читается постоянно и почти не меняется — идеальный кандидат.
Прогресс пользователя (reviews) не кэшируется: он меняется на каждом ответе.

Инвалидация сделана через версионирование ключа, а не через удаление по маске.
Команда KEYS блокирует Redis целиком, а SCAN + DEL по тысячам ключей — лишняя
работа; инкремент версии обесценивает весь старый кэш мгновенно, а записи
отмирают по TTL сами.
"""

import json
import logging
from typing import Any

from app.config import settings
from app.redis_client import redis_client

logger = logging.getLogger(__name__)

_VERSION_KEY = "kanji:cache:version"


async def _version() -> str:
    try:
        value = await redis_client.get(_VERSION_KEY)
        if value is None:
            await redis_client.set(_VERSION_KEY, "1", nx=True)
            return "1"
        return value
    except Exception as exc:  # noqa: BLE001
        # Без Redis работаем напрямую из базы — это медленнее, но корректно.
        logger.warning("Не удалось прочитать версию кэша: %s", exc)
        return "0"


async def bump_version() -> None:
    """Вызывается после изменения справочника (например, из seed.py)."""
    try:
        await redis_client.incr(_VERSION_KEY)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Не удалось инвалидировать кэш: %s", exc)


async def get_json(key: str) -> Any | None:
    try:
        raw = await redis_client.get(f"kanji:v{await _version()}:{key}")
    except Exception as exc:  # noqa: BLE001
        logger.warning("Чтение кэша не удалось: %s", exc)
        return None
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


async def set_json(key: str, value: Any) -> None:
    try:
        await redis_client.set(
            f"kanji:v{await _version()}:{key}",
            json.dumps(value, ensure_ascii=False),
            ex=settings.kanji_cache_ttl_seconds,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Запись в кэш не удалась: %s", exc)
