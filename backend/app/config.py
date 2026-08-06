from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки берутся только из переменных окружения — секретов в коде нет."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    redis_url: str
    environment: Literal["development", "production"] = "development"

    # Лимиты на IP. Запись строже чтения: отправка ответа на карточку меняет
    # состояние SRS, и злоупотребление ей дороже лишнего чтения справочника.
    rate_limit_read_per_minute: int = 60
    rate_limit_write_per_minute: int = 20

    kanji_cache_ttl_seconds: int = 3600

    # Срок жизни куки device_id — год: прогресс не должен теряться от того,
    # что пользователь не заходил месяц.
    device_cookie_max_age_seconds: int = 365 * 24 * 3600
    device_cookie_name: str = "device_id"

    # last_seen_at пишется не чаще этого интервала: иначе каждый GET-запрос
    # превращался бы в запись в базу.
    device_last_seen_throttle_seconds: int = 15 * 60

    # Повторная оценка того же кандзи в этом окне игнорируется — защита от
    # двойного тапа по кнопке на мобильном.
    review_duplicate_window_seconds: int = 3

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def cookie_secure(self) -> bool:
        """Secure-куку браузер не примет по обычному HTTP.

        В production сайт за TLS и флаг нужен, а в локальной разработке он
        привёл бы к тому, что кука молча отбрасывается и на каждый запрос
        заводилось бы новое устройство.
        """
        return self.is_production


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
