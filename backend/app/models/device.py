import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Device(Base):
    """Анонимный пользователь. Аутентификации нет — только идентификатор устройства."""

    __tablename__ = "devices"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Таймзона IANA с клиента (например Europe/Amsterdam). Нужна, чтобы граница
    # суток для дневных счётчиков считалась по месту пользователя: иначе
    # счётчик обнулялся бы посреди его дня. Хранение при этом остаётся в UTC —
    # момент времени и принадлежность к календарному дню это разные вещи.
    timezone: Mapped[str] = mapped_column(
        String(64), nullable=False, server_default="UTC"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
