from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.inline import proxy_loc, type_proxy, rental_period, proxies_kb
from orm_query.proxies import ProxiesRepository
from utils.callbacks import ProxyCatalogCallback

proxy_catalog_router = Router()


@proxy_catalog_router.message(F.text == "Каталог прокси")
async def all_stages_text_message(message: types.Message, session: AsyncSession):
    await countries(callback=message, session=session)


async def countries(**kwargs):
    message = kwargs.get("callback")
    session = kwargs.get("session")
    if isinstance(message, types.Message):
        await message.answer("Вот каталог всех прокси📦 по странам", reply_markup=proxy_loc.as_markup())

    elif isinstance(message, CallbackQuery):
        callback = message
        await callback.message.edit_text("Вот каталог всех прокси📦 по странам", reply_markup=proxy_loc.as_markup())


async def proxy_type(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")
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
    print(db_data)

    if db_data is None:
        await callback.message.edit_text('Извините, прокси под ваши запросы не найдены. '
                                      'Нажмите "Каталог прокси" чтобы найти что-нибудь другое')

    else:
        await callback.message.answer("Вот все доступные прокси под ваши параметры:",
                                      reply_markup=proxies_kb(callback, db_data).as_markup())

async def get_quantity(**kwargs):
    callback = kwargs.get("callback")
    session = kwargs.get("session")
    await callback.message.edit_text("")



@proxy_catalog_router.callback_query(ProxyCatalogCallback.filter())
async def navigate_categories(callback: CallbackQuery, callback_data: ProxyCatalogCallback, session: AsyncSession):
    current_level = callback_data.level

    levels = {
        0: countries,
        1: proxy_type,
        2: period,
        3: get_proxy
    }

    current_level_function = levels[current_level]

    kwargs = {
        "callback": callback,
        "session": session
    }

    await current_level_function(**kwargs)


