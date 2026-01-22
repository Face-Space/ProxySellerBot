from aiogram import Router, F, types
from sqlalchemy.ext.asyncio import AsyncSession

from services.cart import CartService

cart_router = Router()


@cart_router.message(F.text == "Корзина")
async def cart_text_message(message: types.Message, session: AsyncSession):
    await show_cart(message=message, session=session)


async def show_cart(**kwargs):
    message = kwargs.get("message") or kwargs.get("callback")
    session = kwargs.get("session")
    msg, kb_builder = await CartService.create_buttons(message, session)
    if isinstance(message, types.Message):
        await message.answer(msg, reply_markup=kb_builder.as_markup())
