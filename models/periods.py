from pydantic import BaseModel
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class Period(Base):
    __tablename__ = "periods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    period_days: Mapped[str] = mapped_column(String, nullable=False)


class PeriodDTO(BaseModel):
    id: int | None
    period_days: str | None
