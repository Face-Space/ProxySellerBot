from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Integer, ForeignKey, Float, DateTime, Boolean, CheckConstraint, func, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


class Buy(Base):
    __tablename__ = "buys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    buyer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    buyer: Mapped["User"] = relationship("User", back_populates="buys")
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total_price: Mapped[int] = mapped_column(Float, nullable=False)
    buy_datetime: Mapped[DateTime] = mapped_column(DateTime, default=func.date_trunc("second", func.now()))
    is_refunded: Mapped[bool] = mapped_column(Boolean, default=False)
    buys: Mapped[list["BuyProxy"]] = relationship("BuyProxy", back_populates="buy", passive_deletes="all")


    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
        CheckConstraint("total_price > 0", name="check_total_price_positive")
    )

class BuyDTO(BaseModel):
    id: int | None = None
    buyer_id: int | None = None
    quantity: int | None = None
    total_price: float | None = None
    buy_datetime: datetime | None = None
    is_refunded: bool | None = None


class RefundDTO(BaseModel):
    telegram_username: str | None = None
    telegram_id: int | None = None
    subcategory_name: str | None = None
    total_price: float | None = None
    quantity: int | None = None
    buy_id: int | None = None