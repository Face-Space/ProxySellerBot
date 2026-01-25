from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.date_trunc('second', func.now()))
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.date_trunc('second', func.now()),
                                              onupdate=func.date_trunc('second', func.now()))

