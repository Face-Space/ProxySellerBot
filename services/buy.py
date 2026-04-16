from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from orm_query.buy import BuyRepository
from utils.callbacks import MyProfileCallback


class BuyService:

    @staticmethod
    async def get_purchased_item(callback_data: MyProfileCallback, session: AsyncSession) -> tuple[str, InlineKeyboardBuilder]:
        buys = await BuyRepository.get_by_buyer_id(callback_data.buy_id, session)
        msg_text = f"🔹ID покупки: {buys.id}\n📅Время покупки: {buys.buy_datetime}\n💵Оплаченная сумма: {buys.total_price}\n🏷️Скидка: 0 руб.\n🟡Статус: Завершён"
        kb_builder = InlineKeyboardBuilder()
        kb_builder.row(callback_data.get_back_button())
        kb_builder.adjust(1)

        return msg_text, kb_builder
