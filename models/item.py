from pydantic import BaseModel
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base


# class Item(Base):
#     __tablename__ = 'items'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     category_id: Mapped[int] = mapped_column(Integer, ForeignKey("proxies.id", ondelete="CASCADE"), nullable=False)
#     name: Mapped[str] = mapped_column()


class ItemDTO(BaseModel):
    id: int | None = None
    category_id: int | None = None
    private_data: str | None = None
    price: float | None = None
    is_sold: bool | None = None
    is_new: bool | None = None
    description: str | None = None