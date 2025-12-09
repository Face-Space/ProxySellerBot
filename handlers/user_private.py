from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import get_proxy_country, get_proxy
from keyboards.inline import proxy_loc, proxies_kb, type_proxy, rental_period, GlobalData
from keyboards.reply import start_kb



logger = logging.getLogger(__name__)
user_router = Router()


@user_router.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer("Привет👋, я ProxySellerBot🤖, и я помогу тебе выбрать необходимый для тебя прокси!",
                         reply_markup=start_kb)


@user_router.message(F.text == "Каталог прокси")
async def get_country(message: types.Message):

    # далее работает уже с апи
    # proxy_catalog = ProxyProviderClient("https://api.proxy-provider.com", "your-api-key")
    # proxies = proxy_catalog.fetch_products()

    await message.answer("Вот каталог всех прокси📦 по странам", reply_markup=proxy_loc.as_markup())


@user_router.callback_query(F.data.startswith("country"))
async def get_type(callback: types.CallbackQuery,  session: AsyncSession):
    await callback.answer()
    country_name = callback.data.split("_")[1]

    # сохраняем полученный коллбэк в словарь, который потом используем для запроса
    await GlobalData.update_data("country_name", country_name)
    await callback.message.answer("Выберите интересующий вас тип прокси:", reply_markup=type_proxy.as_markup())


@user_router.callback_query(F.data.startswith("name"))
async def get_period(callback: types.CallbackQuery):
    await callback.answer()
    proxy_type = callback.data.split("_")[1]
    await GlobalData.update_data("proxy_type", proxy_type)
    await callback.message.answer("Отлично, теперь укажите желаемый срок аренды прокси:", reply_markup=rental_period.as_markup())


@user_router.callback_query(F.data.startswith("period"))
async def get_quantity(session: AsyncSession, callback: types.CallbackQuery):
    await callback.answer()
    period_rental = callback.data.split("_")[1]
    await GlobalData.update_data("period_rental", period_rental)

    await get_proxy(session, GlobalData.data)
    await callback.message.answer("Вот все доступные прокси под ваши параметры:")


@user_router.message(~Command("admin"))
async def delete_trash(message: types.Message):
    await message.delete()


