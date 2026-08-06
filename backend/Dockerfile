FROM python:3.12-slim

# Не писать .pyc и не буферизовать вывод — иначе логи в docker logs отстают.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Зависимости отдельным слоем: пересобираются только при изменении requirements.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Работаем не от root: у процесса нет причин иметь права суперпользователя.
RUN useradd --create-home --uid 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Команда запуска задана в docker-compose.yml, чтобы флаги uvicorn были видны
# рядом с публикацией порта.
