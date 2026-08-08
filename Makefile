# Короткие команды вместо длинных строк docker compose.
#
# Смысл не в экономии символов, а в том, что порядок шагов перестаёт быть
# знанием в голове. Например, справочник надо собрать И залить — забыть второе
# легко, и тогда правка просто не доедет до приложения; здесь для этой пары
# есть одна цель `content`.

# read -s для скрытого ввода пароля — не POSIX, в /bin/sh его может не быть.
SHELL    := /bin/bash

DC       := docker compose
DC_DEV   := docker compose -f docker-compose.yml -f docker-compose.dev.yml
BACKEND  := $(DC) run --rm backend
# Хостовый интерпретатор для скриптов, которые не ходят в базу. На macOS и в
# свежих дистрибутивах голого `python` в PATH нет — только python3. Внутри
# venv переопределяется: make translate PY=python
PY       ?= python3
# Сборка справочника пишет в data/, а он смонтирован на чтение в базовом
# файле — поэтому только через dev-конфигурацию.
BACKEND_RW := $(DC_DEV) run --rm backend

.DEFAULT_GOAL := help

.PHONY: help up down restart logs ps dev migrate revision seed dataset content \
        translate review attribution shell psql check

help: ## Показать список команд
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

# --- Стек ---------------------------------------------------------------

up: ## Поднять стек
	$(DC) up -d

down: ## Остановить стек (данные сохраняются)
	$(DC) down

restart: ## Пересобрать и перезапустить
	$(DC) up -d --build

logs: ## Логи всех сервисов, последние 100 строк
	$(DC) logs -f --tail=100

ps: ## Состояние контейнеров
	$(DC) ps

dev: ## Поднять стек с монтированием исходников и авто-перезагрузкой
	$(DC_DEV) up -d

# --- База ---------------------------------------------------------------

migrate: ## Накатить миграции
	$(BACKEND) alembic upgrade head

revision: ## Создать миграцию: make revision M="описание"
	@test -n "$(M)" || (echo "нужно: make revision M=\"описание\"" && exit 1)
	$(DC_DEV) run --rm backend alembic revision --autogenerate -m "$(M)"

psql: ## Консоль psql
	$(DC) exec db psql -U $${POSTGRES_USER:-kanji} -d $${POSTGRES_DB:-everyday_kanji}

# --- Контент ------------------------------------------------------------

dataset: ## Пересобрать backend/data/kanji.json из источников
	$(BACKEND_RW) python -m scripts.build_dataset

seed: ## Залить справочник в базу
	$(BACKEND) python -m scripts.seed

content: dataset seed ## Пересобрать справочник И залить его (обычно нужна именно эта пара)

translate: ## Перевести значения: make translate LIMIT=30
	@test -f .env.scripts || (echo "нет .env.scripts с ANTHROPIC_API_KEY — см. docs/kanji-pipeline.md" && exit 1)
	set -a && . ./.env.scripts && set +a && \
		cd backend && $(PY) -m scripts.etl.translate_meanings --limit $(or $(LIMIT),30)

review: ## Вычитать машинный перевод (интерактивно)
	cd backend && $(PY) -m scripts.review_meanings $(if $(FROM),--from $(FROM),)

attribution: ## Перегенерировать ATTRIBUTION.md из app/sources.py
	cd backend && $(PY) -m scripts.render_attribution

# --- Прочее -------------------------------------------------------------

admin-password: ## Задать пароль к админке: make admin-password ADMIN_USER=имя
	@# ADMIN_USER, а не USER: USER есть в окружении любой оболочки, и проверка
	@# на пустоту никогда бы не срабатывала — имя молча бралось бы системное.
	@test -n "$(ADMIN_USER)" || (echo "нужно: make admin-password ADMIN_USER=имя" && exit 1)
	@# Хэш считает контейнер httpd: на хосте не нужен apache2-utils, а bcrypt
	@# (-B) не обрезает пароль до восьми значащих символов, как старый crypt.
	@read -rsp "пароль для $(ADMIN_USER): " pw; echo; \
		printf '%s' "$$pw" \
		| docker run --rm -i httpd:2.4-alpine htpasswd -niB "$(ADMIN_USER)" \
		| head -1 > nginx/.htpasswd
	@echo "записано в nginx/.htpasswd — применить: make up"

shell: ## Консоль внутри контейнера бэкенда
	$(BACKEND) sh

check: ## Быстрая проверка живости стека
	@curl -sf http://127.0.0.1:$${APP_PORT:-8082}/api/health >/dev/null \
		&& echo "  api    ок" || echo "  api    НЕ ОТВЕЧАЕТ"
	@curl -sf -o /dev/null http://127.0.0.1:$${APP_PORT:-8082}/ \
		&& echo "  фронт  ок" || echo "  фронт  НЕ ОТВЕЧАЕТ"
	@cd backend && $(PY) -m scripts.render_attribution --check >/dev/null \
		&& echo "  атрибуция ок" || echo "  ATTRIBUTION.md устарел (make attribution)"
