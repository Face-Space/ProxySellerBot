from enums.keyboard_button import KeyboardButton
from pydantic import BaseModel
from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class ButtonMedia(Base):
    __tablename__ = "buttons_media"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    media_id: Mapped[int] = mapped_column(String, nullable=False)
    button: Mapped[Enum[KeyboardButton]] = mapped_column(Enum(KeyboardButton), unique=True)


class ButtonMediaDTO(BaseModel):
    id: int | None = None
    media_id: str | None = None
    button: KeyboardButton | None = None
