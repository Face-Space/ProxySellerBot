from pydantic import BaseModel
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base
# from models.buy import Buy


class BuyProxy(Base):
    __tablename__ = "buyProxy"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    buy_id: Mapped[int] = mapped_column(Integer, ForeignKey("buys.id", ondelete="CASCADE"), nullable=False)
    buy: Mapped["Buy"] = relationship("Buy", back_populates="buys")
    proxy_id: Mapped[int] = mapped_column(Integer, ForeignKey("proxies.id", ondelete="CASCADE"), nullable=False)
    proxy: Mapped["Proxies"] = relationship("Proxies", back_populates="proxies")


class BuyProxyDTO(BaseModel):
    id: int | None = None
    buy_id: int | None = None
    proxy_id: int | None = None

