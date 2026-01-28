from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class Country(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(primary_key=True)
    country_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    country_flag: Mapped[str] = mapped_column(String, nullable=False, unique=True)


class CountryDTO(BaseModel):
    id: int | None = None
    country_name: str | None = None
    country_flag: str | None = None