from pydantic import BaseModel
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class ProxyType(Base):
    __tablename__ = "proxy_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    proxy_type: Mapped[str] = mapped_column(String, nullable=False)


class ProxyTypeDTO(BaseModel):
    id: int | None
    proxy_type: str | None
