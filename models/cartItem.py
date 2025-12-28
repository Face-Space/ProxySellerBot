from pydantic import BaseModel
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    # name: Mapped[str] = mapped_column(ForeignKey("proxies.name"))
    # proxy_type: Mapped[str] = mapped_column(ForeignKey("proxies.proxy_type"))
    # country: Mapped[str] = mapped_column(ForeignKey("proxies.country"))
    # period_days: Mapped[int] = mapped_column(ForeignKey("proxies.period_days"))
    quantity: Mapped[int] = mapped_column(ForeignKey("proxies.quantity"))
    # price: Mapped[int] = mapped_column(ForeignKey("proxies.price"))


class CartItemDTO(BaseModel):
    id: int | None = None
    cart_id: int | None = None
    quantity: int | None = None

