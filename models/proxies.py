from sqlalchemy import func, DateTime, String, Integer, Float, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from models.base import Base


class Proxies(Base):
    __tablename__ = "proxies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    proxy_type: Mapped[str] = mapped_column(String(10), nullable=False)
    country: Mapped[str] = mapped_column(String(30), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

