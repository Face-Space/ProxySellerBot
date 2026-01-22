from aiogram import types, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile
import logging

import config
from config import ADMIN_ID_LIST

logger = logging.getLogger(__name__)

class NotificationService:

    @staticmethod
    async def send_to_admins(message: str | BufferedInputFile, reply_markup: types.InlineKeyboardMarkup | None):

        bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        for admin_id in ADMIN_ID_LIST:
            try:
                if isinstance(message, str):
                    await bot.send_message(admin_id, f"<b>{message}</b>", reply_markup=reply_markup)
                else:
                    await bot.send_document(admin_id, message, reply_markup=reply_markup)
            except Exception as e:
                logger.error(e)

