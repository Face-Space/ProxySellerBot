from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Integer, String, Float, DateTime, func, Boolean, CheckConstraint, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_username: Mapped[str] = mapped_column(String, unique=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    top_up_amount: Mapped[int] = mapped_column(Float, default=0.0)
    consume_records: Mapped[int] = mapped_column(Float, default=0.0)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    can_receive_messages: Mapped[int] = mapped_column(Boolean, default=True)

    __table_args__ = (
        CheckConstraint('top_up_amount >= 0', name='check_top_up_amount_positive'),
        CheckConstraint('consume_records >= 0', name='check_consume_records_positive'),
    )


class UserDTO(BaseModel):
    id: int | None = None
    telegram_username: str | None = None
    telegram_id: int | None = None
    top_up_amount: float | None = None
    consume_records: float | None = None
    registered_at: datetime | None = None
    can_receive_messages: bool | None = None