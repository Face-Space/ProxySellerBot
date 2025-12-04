from aiogram import Router, types, Dispatcher, F
from aiogram.filters import Command, CommandStart
import logging

from keyboards.reply import start_kb



logger = logging.getLogger(__name__)
user_router = Router()


@user_router.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer("Привет👋, я ProxySellerBot🤖, и я помогу тебе выбрать необходимый для тебя прокси!",
                         reply_markup=start_kb)


@user_router.message(F.text == "Каталог прокси")
async def catalog_proxy(message: types.Message):
    await message.answer("Вот каталог всех прокси. Выберите фильтры и товар📦")



@user_router.message(~Command("admin"))
async def delete_trash(message: types.Message):
    await message.delete()


