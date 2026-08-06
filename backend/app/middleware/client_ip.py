"""Определение реального IP клиента.

Бэкенд стоит за двумя прокси: nginx на хосте → контейнер. Если не разобрать
заголовки, все запросы придут с 127.0.0.1, лимитер посчитает их одним клиентом
и забанит всех разом.

Основной путь — uvicorn с --proxy-headers, который сам подставляет адрес из
X-Forwarded-For в request.client.host. Разбор заголовков здесь — подстраховка
на случай, если флаг потеряется.

Важно про доверие: --forwarded-allow-ips="*" означает «верю заголовку от кого
угодно». Это безопасно ровно потому, что контейнер опубликован на 127.0.0.1 и
недоступен извне. Если порт когда-нибудь откроют шире, клиент сможет подделать
свой адрес и обойти лимитер.
"""

from starlette.requests import Request

_LOCAL = {"127.0.0.1", "::1", "localhost"}


def get_client_ip(request: Request) -> str:
    direct = request.client.host if request.client else None

    # Если uvicorn уже подставил внешний адрес — доверяем ему.
    if direct and direct not in _LOCAL:
        return direct

    # X-Real-IP предпочтительнее: nginx его перезаписывает, тогда как
    # X-Forwarded-For дописывается, и левый элемент списка контролируется
    # клиентом, то есть подделывается.
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()

    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        # Берём последний элемент — он добавлен ближайшим доверенным прокси.
        parts = [p.strip() for p in forwarded.split(",") if p.strip()]
        if parts:
            return parts[-1]

    return direct or "unknown"
