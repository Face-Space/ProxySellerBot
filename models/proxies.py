from sqlalchemy import func, DateTime, String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from models.base import Base


class Proxies(Base):
    __tablename__ = "proxies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(15))
    proxy_type: Mapped[str] = mapped_column(String(10))
    country: Mapped[str] = mapped_column(String(15))
    period_days: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)

