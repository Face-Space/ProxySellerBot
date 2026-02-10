from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from services.cart import CartService
from utils.callbacks import CartCallback

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

    elif isinstance(message, types.Message):
        callback = message
        await callback.message.edit_text(msg, reply_markup=kb_builder.as_markup())


async def delete_cart_item(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")
    msg, kb_builder = await CartService.delete_cart_item(callback, session)
    await callback.message.edit_text(text=msg, reply_markup=kb_builder.as_markup())


async def checkout_processing(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")
    msg, kb_builder = await CartService.checkout_processing(callback, session)
    await callback.message.edit_text(text=msg, reply_markup=kb_builder.as_markup())


async def buy_processing(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")
    await callback.message.edit_reply_markup() # Блокируем старые кнопки т.к. мб код ниже будет совершаться долго
    # перед тем как дойдёт до edit_text()
    msg, kb_builder = await CartService.buy_processing(callback, session)
    await callback.message.edit_text(text=msg, reply_markup=kb_builder.as_markup())


@cart_router.callback_query(CartCallback.filter())
async def navigate_cart_progress(callback: CallbackQuery, callback_data: CartCallback, session: AsyncSession):
    current_level = callback_data.level

    level = {
        0: show_cart,
        1: delete_cart_item,
        2: checkout_processing,
        3: buy_processing
    }

    current_level_function = level[current_level]

    kwargs = {
        "callback": callback,
        "session": session
    }

    await current_level_function(**kwargs)

