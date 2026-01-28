from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

# from keyboards.inline import proxy_loc, type_proxy, rental_period, proxies_kb, proxy_quantity
from orm_query.proxies import ProxiesRepository
from services.cart import CartService
from services.country import CountryService
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
    msg, kb_builder = await ProxyTypeService.get_buttons(session, callback)


    await callback.message.edit_text("Выберите интересующий вас тип прокси:", reply_markup=type_proxy(callback).as_markup())


async def period(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")
    await callback.message.edit_text("Отлично, теперь укажите желаемый срок аренды прокси:",
                                     reply_markup=rental_period(callback).as_markup())


async def get_proxy(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")

    db_data = await ProxiesRepository.get_proxy(callback, session)

    if db_data is None:
        await callback.message.edit_text('Извините, прокси под ваши запросы не найдены. '
                                      'Нажмите "Каталог прокси" чтобы найти что-нибудь другое')

    else:
        await callback.message.edit_text("Вот все доступные прокси под ваши параметры:",
                                      reply_markup=proxies_kb(callback, db_data).as_markup())


async def get_quantity(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")
    await callback.message.edit_text("Теперь выберите необходимое количество прокси из доступно возможных",
                                     reply_markup=proxy_quantity(callback).as_markup())


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
        2: period,
        3: get_proxy,
        4: get_quantity,
        5: add_to_cart
    }

    current_level_function = levels[current_level]

    kwargs = {
        "callback": callback,
        "session": session
    }

    await current_level_function(**kwargs)


