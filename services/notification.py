from aiogram import types
from aiogram.types import BufferedInputFile
import logging

from bot_setup import bot
from config import ADMIN_ID_LIST

logger = logging.getLogger(__name__)

class NotificationService:

    @staticmethod
    async def send_to_admins(message: str | BufferedInputFile, reply_markup: types.InlineKeyboardMarkup | None):

        for admin_id in ADMIN_ID_LIST:
            try:
                if isinstance(message, str):
                    await bot.send_message(admin_id, f"<b>{message}</b>", reply_markup=reply_markup)
                else:
                    await bot.send_document(admin_id, message, reply_markup=reply_markup)
            except Exception as e:
                logger.error(e)

