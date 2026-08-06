"""Работа с локальными сутками устройства.

Хранение времени всегда в UTC. Но принадлежность к календарному дню считается
в таймзоне пользователя: иначе счётчик «сделано за сегодня» обнулялся бы
посреди его дня.
"""

from datetime import UTC, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def safe_zone(name: str | None) -> ZoneInfo:
    """Таймзона приходит с клиента, поэтому произвольная строка не должна ронять запрос."""
    if not name:
        return ZoneInfo("UTC")
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError):
        return ZoneInfo("UTC")


def is_valid_zone(name: str | None) -> bool:
    if not name:
        return False
    try:
        ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError):
        return False
    return True


def local_day_start_utc(tz_name: str | None, now: datetime | None = None) -> datetime:
    """Начало текущих локальных суток устройства, выраженное в UTC.

    Именно это значение подставляется в запросы: сравнение идёт с полем
    TIMESTAMPTZ, которое хранится в UTC.
    """
    tz = safe_zone(tz_name)
    now = (now or datetime.now(UTC)).astimezone(tz)
    start_local = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_local.astimezone(UTC)
