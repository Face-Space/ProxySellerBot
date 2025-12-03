from aiogram import Router, types, Dispatcher
from aiogram.filters import Command, CommandStart
import logging


logger = logging.getLogger(__name__)
user_router = Router()


@user_router.message(CommandStart())
async def start_bot(message: types.Message):
    await message.answer("Привет, я ProxySellerBot, и я помогу тебе выбрать необходимый для тебя прокси!")


