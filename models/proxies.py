from sqlalchemy import func, DateTime, String, Integer, Float, Numeric, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from models.base import Base


class Proxies(Base):
    __tablename__ = "proxies"

    id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("countries.id", ondelete="CASCADE"), nullable=False)

    name: Mapped[str] = mapped_column(String, nullable=False)
    proxy_type_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    # is_sold: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
