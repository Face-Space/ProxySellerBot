import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.payment import Payment


class PaymentRepository:

    @staticmethod
    async def create(payment_id: int, user_id: int, message_id: int, session: AsyncSession):
        payment = Payment(
            processing_payment_id=payment_id,
            user_id=user_id,
            message_id=message_id,
            expire_datetime=datetime.datetime.now() + datetime.timedelta(hours=1),
            is_paid=False
        )
        session.add(payment)

    @staticmethod
    async def get_unexpired_unpaid_payments(user_id: int, session: AsyncSession):
        sub_stmt = (select(Payment)
                    .where(Payment.expire_datetime > datetime.datetime.now(),
                           Payment.user_id == user_id,
                           Payment.is_paid == False)).subquery()
        stmt = select(func.count()).select_from(sub_stmt)
        count = await session.execute(stmt)
        return count.scalar_one()
