from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import get_proxy_country
from keyboards.inline import proxy_loc, proxies_kb
from keyboards.reply import start_kb



logger = logging.getLogger(__name__)
user_router = Router()


@user_router.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer("Привет👋, я ProxySellerBot🤖, и я помогу тебе выбрать необходимый для тебя прокси!",
                         reply_markup=start_kb)


@user_router.message(F.text == "Каталог прокси")
async def catalog_proxy(message: types.Message):

    # далее работает уже с апи
    # proxy_catalog = ProxyProviderClient("https://api.proxy-provider.com", "your-api-key")
    # proxies = proxy_catalog.fetch_products()

    await message.answer("Вот каталог всех прокси📦 по странам", reply_markup=proxy_loc.as_markup())


@user_router.callback_query(F.data.startswith("страна"))
async def get_country(callback: types.CallbackQuery,  session: AsyncSession):
    await callback.answer()
    country = callback.data.split("_")[1]
    data = await get_proxy_country(session, f"{country}")
    await callback.message.answer(f"Вот все прокси из страны {country}:", reply_markup=proxies_kb(data[0].name).as_markup())



@user_router.message(~Command("admin"))
async def delete_trash(message: types.Message):
    await message.delete()


