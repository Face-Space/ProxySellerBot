# cart is a container for unsold items to collect items from different countries (proxy_types)
# to be able to checkout this cart at once together with a shipment fee. Only the
# quantity, category, subcategory is stored because the unique item is not yet sold
#
# note that the item is NOT reserved or blocked so that the availability of the item
# needs to be checked again during checkout
from pydantic import BaseModel
from sqlalchemy import Integer, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'), nullable=False)
    # ForeignKey('users.id') означает, что мы можем вставить в carts.user_id только существующие значения из users.id
    # А также ForeignKey указывает кто является родителем, а кто ребёнком
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

class CartDTO(BaseModel):
    id: int | None = None
    user_id: int | None = None
