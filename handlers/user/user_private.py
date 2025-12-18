from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
import logging

from aiogram.types import LabeledPrice
from sqlalchemy.ext.asyncio import AsyncSession

import config
from bot_setup import bot
from handlers.user.proxy_catalog import proxy_catalog_router
from keyboards.reply import start_kb
from models.user import UserDTO
from services.user import UserService

logger = logging.getLogger(__name__)
user_router = Router()
user_router.include_routers(
    proxy_catalog_router
)


@user_router.message(CommandStart())
async def start_bot(message: types.Message, session: AsyncSession):
    await message.answer("Привет👋, я ProxySellerBot🤖, и я помогу тебе выбрать необходимый для тебя прокси!",
                         reply_markup=start_kb)
    telegram_id = message.from_user.id
    await UserService.create_if_not_exist(UserDTO(
        telegram_username=message.from_user.username,
        telegram_id=telegram_id
    ), session)
    # безопасное извлечения/валидация пользовательских данных из сессии БД перед обработкой сообщений





@user_router.message(~Command("admin"))
async def delete_trash(message: types.Message):
    await message.delete()


