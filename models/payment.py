from pydantic import BaseModel
from sqlalchemy import Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

import config
from enums.cryptocurrency import Cryptocurrency
from enums.currency import Currency
from enums.payment import PaymentType
from models import Base


class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="payments")
    processing_payment_id: Mapped[int] = mapped_column(Integer, nullable=False)
    message_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_paid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    expire_datetime: Mapped[DateTime] =  mapped_column(DateTime(timezone=True))

    def __repr__(self):
        return f"Payment ID:{self.id}"


class ProcessingPaymentDTO(BaseModel):
    id: int | None = None
    paymentType: PaymentType = PaymentType.DEPOSIT
    fiatCurrency: str | None = None
    fiatAmount: float | None = None
    cryptoAmount: float | None = None
    userId: str | None = None
    cryptoCurrency: Cryptocurrency
    expireDatetime: int | None = None
    createDatetime: int | None = None
    address: str | None = None
    isPaid: bool | None = None
    isWithdrawn: bool | None = None
    hash: str | None = None
    # callbackUrl: str = f'{config.WEBHOOK_URL}cryptoprocessing/event'
    callbackSecret: str | None = config.KRYPTO_EXPRESS_API_SECRET if len(config.KRYPTO_EXPRESS_API_SECRET) > 0 else None
