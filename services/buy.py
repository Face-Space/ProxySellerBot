from datetime import timedelta

from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from orm_query.buy import BuyRepository
from services.proxy_type import ProxyService
from utils.callbacks import MyProfileCallback


class BuyService:

    @staticmethod
    async def get_purchased_item(callback_data: MyProfileCallback, session: AsyncSession) -> tuple[str, InlineKeyboardBuilder]:
        buys = await BuyRepository.get_by_buyer_id(callback_data.buy_id, session)
        days_count = await ProxyService.calculate_days(buys.period_days)
        msg_text = (f"🔹ID покупки: {buys.id}\n📅Время покупки: {buys.buy_datetime}\n "
                    f"🕓Срок истечения прокси: \n{buys.buy_datetime + timedelta(days=days_count)},"
                    f" \n💵Оплаченная сумма: {buys.total_price}"
                    f"\n📦Количество прокси: {buys.quantity}.\n🏷️Скидка: 0 руб.\n🟡Статус: Завершён")
        kb_builder = InlineKeyboardBuilder()
        kb_builder.row(callback_data.get_back_button())
        kb_builder.adjust(1)

        return msg_text, kb_builder
