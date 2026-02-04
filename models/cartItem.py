from pydantic import BaseModel
from sqlalchemy import Integer, ForeignKey, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    proxy_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    country_id: Mapped[int] = mapped_column(Integer, nullable=False)
    period_days: Mapped[str] = mapped_column(String)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)


class CartItemDTO(BaseModel):
    id: int | None = None
    cart_id: int | None = None
    name: str | None = None
    proxy_type_id: int | None = None
    country_id: int | None = None
    period_days: str | None = None
    quantity: int | None = None
    price: float | None = None


