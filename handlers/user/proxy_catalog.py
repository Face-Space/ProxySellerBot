from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from services.cart import CartService
from services.country import CountryService
from services.proxy_type import ProxyService
from utils.callbacks import ProxyCatalogCallback

proxy_catalog_router = Router()


@proxy_catalog_router.message(F.text == "Каталог прокси")
async def all_stages_text_message(message: types.Message, session: AsyncSession):
    await countries(callback=message, session=session)


async def countries(**kwargs):
    message = kwargs.get("callback")
    session = kwargs.get("session")
    if isinstance(message, types.Message):
        msg, kb_builder = await CountryService.get_buttons(session)
        await message.answer(msg, reply_markup=kb_builder.as_markup())

    elif isinstance(message, CallbackQuery):
        callback = message
        msg, kb_builder = await CountryService.get_buttons(session, callback)
        await callback.message.edit_text(msg, reply_markup=kb_builder.as_markup())


async def show_proxy_type(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")
    msg, kb_builder = await ProxyService.get_buttons(callback, session)
    await callback.message.edit_text(msg, reply_markup=kb_builder.as_markup())


async def show_proxies(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")
    msg, kb_builder = await ProxyService.show_filtered_proxies(callback, session)
    await callback.message.edit_text(msg, reply_markup=kb_builder.as_markup())


async def select_quantity(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")
    msg, kb_builder = await ProxyService.get_select_quantity_buttons(callback, session)
    await callback.message.edit_text(msg, reply_markup=kb_builder.as_markup())


async def select_period(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")
    msg, kb_builder = await ProxyService.get_select_period_buttons(callback, session)
    await callback.message.edit_text(msg, reply_markup=kb_builder.as_markup())


async def add_to_cart_confirmation(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")
    msg, kb_builder = await ProxyService.get_add_to_cart_buttons(callback, session)
    await callback.message.edit_text(text=msg, reply_markup=kb_builder.as_markup())


async def add_to_cart(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")
    await CartService.add_to_cart(callback, session)
    await callback.message.edit_text("Товар добавлен в корзину")


@proxy_catalog_router.callback_query(ProxyCatalogCallback.filter())
async def navigate_categories(callback: CallbackQuery, callback_data: ProxyCatalogCallback, session: AsyncSession):
    current_level = callback_data.level

    levels = {
        0: countries,
        1: show_proxy_type,
        2: show_proxies,
        3: select_quantity,
        4: select_period,
        5: add_to_cart_confirmation,
        6: add_to_cart
    }

    current_level_function = levels[current_level]

    kwargs = {
        "callback": callback,
        "session": session
    }

    await current_level_function(**kwargs)


