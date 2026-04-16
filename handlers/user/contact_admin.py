from aiogram import Router, F
from aiogram.types import Message


contact_router = Router()


@contact_router.message(F.text == "Связь с админом")
async def contact_admin(message: Message):
    await message.answer("По любым вопросам, касаемо бота можете связаться с админом @paralllaxx")

