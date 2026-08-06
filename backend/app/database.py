from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(DeclarativeBase):
    """Общий базовый класс моделей.

    Схему создаёт только Alembic; Base.metadata.create_all не используется
    нигде — иначе схема начнёт расходиться с историей миграций.
    """


engine = create_async_engine(
    settings.database_url,
    # pool_pre_ping спасает от «протухших» соединений после простоя или
    # перезапуска базы: соединение проверяется перед выдачей из пула.
    pool_pre_ping=True,
    echo=False,
)

session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    # Объекты остаются доступными после commit — иначе обращение к полям
    # уже сохранённой модели вызвало бы повторный запрос к базе.
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость FastAPI: сессия на время обработки запроса."""
    async with session_factory() as session:
        yield session
