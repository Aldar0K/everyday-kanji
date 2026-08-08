"""Ограничение частоты запросов.

API публичный и без аутентификации, поэтому лимитер обязателен.

Ключ строится по IP, а не по device_id: последний выдаёт сам сервер по первому
запросу, то есть подделывается тривиально.

INCR и EXPIRE выполняются одним Lua-скриптом. По отдельности они не атомарны:
если процесс упадёт между ними, ключ останется без TTL и заблокирует адрес
навсегда.
"""

import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.config import settings
from app.middleware.client_ip import get_client_ip
from app.redis_client import redis_client

logger = logging.getLogger(__name__)

# Возвращает текущее значение счётчика, выставляя TTL при первом инкременте.
_LUA_INCR = """
local current = redis.call('INCR', KEYS[1])
if current == 1 then
  redis.call('EXPIRE', KEYS[1], ARGV[1])
end
return current
"""

_WINDOW_SECONDS = 60
_WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:  # noqa: ANN001
        super().__init__(app)
        self._script = None

    async def dispatch(self, request: Request, call_next):  # noqa: ANN001, ANN201
        # Health-check не лимитируем: он нужен для мониторинга и не нагружает базу.
        #
        # Админку тоже: одна её страница тянет десяток файлов статики, и лимит
        # в 60 запросов в минуту выбирался бы за пару переходов. Публично она
        # не открыта — доступ закрыт HTTP Basic в nginx, а лимитер защищает от
        # анонимной нагрузки, которой здесь нет.
        if request.url.path == "/api/health" or request.url.path.startswith("/admin"):
            return await call_next(request)

        is_write = request.method in _WRITE_METHODS
        limit = (
            settings.rate_limit_write_per_minute
            if is_write
            else settings.rate_limit_read_per_minute
        )
        bucket = "w" if is_write else "r"
        key = f"rl:{bucket}:{get_client_ip(request)}"

        try:
            if self._script is None:
                self._script = redis_client.register_script(_LUA_INCR)
            current = int(await self._script(keys=[key], args=[_WINDOW_SECONDS]))
        except Exception as exc:  # noqa: BLE001
            # Fail-open: Redis без персистентности и может перезапуститься.
            # Ронять всё приложение из-за счётчика хуже, чем на минуту
            # остаться без лимита.
            logger.warning("Лимитер недоступен, пропускаем запрос: %s", exc)
            return await call_next(request)

        if current > limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Слишком много запросов, попробуйте позже."},
                headers={"Retry-After": str(_WINDOW_SECONDS)},
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(max(0, limit - current))
        return response
