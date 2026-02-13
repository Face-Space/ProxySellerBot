from pydantic import BaseModel
from sqlalchemy import func, DateTime, String, Integer, Float, Numeric, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from models.base import Base


# from models.buyProxy import BuyProxy


class Proxies(Base):
    __tablename__ = "proxies"

    id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)

    name: Mapped[str] = mapped_column(String, nullable=False)
    proxy_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    proxies: Mapped[list["BuyProxy"]] = relationship("BuyProxy", back_populates="proxy", passive_deletes="all")
                                                     # cascade="all, delete-orphan"


class ProxyDTO(BaseModel):
    id: int | None = None
    country_id: int | None = None
    name: str | None = None
    proxy_type_id: int | None = None
    quantity: int | None = None
    price: float | None = None
