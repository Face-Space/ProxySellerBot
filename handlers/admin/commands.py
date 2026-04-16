from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from asgiref.sync import sync_to_async

from config import ADMIN_ID_LIST
from utils.custom_filters import AdminFilter


admin_router = Router()
@admin_router.message(Command("admin"), AdminFilter())
async def admin_stats(message: Message):
    # count = await sync_to_async(TelegramUser.objects.count)()
    bot = message.bot
    for admin_id in ADMIN_ID_LIST:
        await bot.send_message(admin_id , f"Вот ссылка в вашу админку: ")
        # python manage.py runserver
        # AdminFilter?
        # а мне теперь надо заново создавать superuser для админки после миграции с существующими таблицами?
