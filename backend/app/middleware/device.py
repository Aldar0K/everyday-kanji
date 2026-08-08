"""Идентификация устройства через httpOnly-куку.

Кука, а не localStorage: она недоступна JavaScript и потому не утекает при XSS.

Два нюанса, которые легко упустить:

1. Флаг Secure включается только в production. По обычному HTTP браузер
   Secure-куку молча отбрасывает, и в локальной разработке на каждый запрос
   заводилось бы новое устройство.

2. last_seen_at обновляется не чаще, чем раз в заданный интервал. Иначе каждый
   GET-запрос превращался бы в запись в базу — лишняя нагрузка и блокировки
   на ровном месте. Дроссель держим в Redis.
"""

import logging
import uuid

from sqlalchemy import select, update
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.config import settings
from app.database import session_factory
from app.models import Device
from app.redis_client import redis_client
from app.services.timezone import is_valid_zone

logger = logging.getLogger(__name__)

_TZ_HEADER = "x-timezone"


class DeviceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # noqa: ANN001, ANN201
        # На health-check устройство не заводим: иначе любой мониторинг
        # плодил бы строки в devices.
        if request.url.path == "/api/health":
            return await call_next(request)

        raw = request.cookies.get(settings.device_cookie_name)
        device_id = _parse_uuid(raw)
        is_new = device_id is None

        client_tz = request.headers.get(_TZ_HEADER)
        client_tz = client_tz if is_valid_zone(client_tz) else None

        if is_new:
            device_id = uuid.uuid4()
            await _create_device(device_id, client_tz)
        else:
            await _touch_device(device_id, client_tz)

        request.state.device_id = device_id

        response = await call_next(request)

        if is_new:
            response.set_cookie(
                key=settings.device_cookie_name,
                value=str(device_id),
                max_age=settings.device_cookie_max_age_seconds,
                httponly=True,
                secure=settings.cookie_secure,
                samesite="lax",
                path="/",
            )
        return response


def _parse_uuid(raw: str | None) -> uuid.UUID | None:
    if not raw:
        return None
    try:
        return uuid.UUID(raw)
    except (ValueError, AttributeError, TypeError):
        return None


async def _create_device(device_id: uuid.UUID, tz: str | None) -> None:
    async with session_factory() as session:
        session.add(Device(id=device_id, timezone=tz or "UTC"))
        await session.commit()


async def _touch_device(device_id: uuid.UUID, tz: str | None) -> None:
    """Обновляет last_seen_at не чаще, чем раз в интервал.

    Смена таймзоны при этом применяется сразу, а не ждёт окончания интервала:
    устройство часто создаётся на первом запросе, когда клиент ещё не прислал
    заголовок, и без этого исключения оно осталось бы в UTC на все 15 минут —
    с неверной границей суток для дневных счётчиков.

    Чтобы не делать ради этой проверки лишний SELECT, последнее известное
    значение таймзоны держим прямо в ключе дросселя.
    """
    throttle_key = f"device:seen:{device_id}"
    try:
        cached = await redis_client.get(throttle_key)
        if cached is None:
            should_write = True
        else:
            should_write = bool(tz) and tz != cached
    except Exception as exc:  # noqa: BLE001
        logger.warning("Дроссель last_seen_at недоступен: %s", exc)
        return

    if not should_write:
        return

    try:
        await redis_client.set(
            throttle_key,
            tz or "UTC",
            ex=settings.device_last_seen_throttle_seconds,
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Не удалось обновить ключ дросселя: %s", exc)

    async with session_factory() as session:
        values: dict = {"last_seen_at": _now()}
        if tz:
            values["timezone"] = tz
        result = await session.execute(
            update(Device).where(Device.id == device_id).values(**values)
        )
        # Куку могли принести от устройства, которого нет в базе (например,
        # после пересоздания тома). Тогда заводим запись заново, сохранив id,
        # чтобы прогресс не «переехал» на новый идентификатор.
        if result.rowcount == 0:
            exists = await session.scalar(select(Device.id).where(Device.id == device_id))
            if exists is None:
                session.add(Device(id=device_id, timezone=tz or "UTC"))
        await session.commit()


def _now():  # noqa: ANN202
    from datetime import UTC, datetime

    return datetime.now(UTC)
