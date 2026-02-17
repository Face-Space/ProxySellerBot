from aiogram import types, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile, InlineKeyboardMarkup
import logging

from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

import config
from config import ADMIN_ID_LIST
from models.cartItem import CartItemDTO
from models.proxies import ProxyDTO
from models.user import UserDTO
from orm_query.country import CountryRepository
from orm_query.proxies import ProxiesRepository
from orm_query.proxy_type import ProxyTypeRepository

logger = logging.getLogger(__name__)

class NotificationService:

    @staticmethod
    async def make_user_button(username: str | None) -> InlineKeyboardMarkup:
        user_button_builder = InlineKeyboardBuilder()
        if username:
            user_button_inline = types.InlineKeyboardButton(text=username, url=f"https://t.me/{username}")
            user_button_builder.add(user_button_inline)
        return user_button_builder.as_markup()

    @staticmethod
    async def send_to_admins(message: str | BufferedInputFile, reply_markup: types.InlineKeyboardMarkup | None):
        async with Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) as bot:
            for admin_id in ADMIN_ID_LIST:
                try:
                    if isinstance(message, str):
                        await bot.send_message(admin_id, f"<b>{message}</b>", reply_markup=reply_markup)
                    else:
                        await bot.send_document(admin_id, message, reply_markup=reply_markup)
                except Exception as e:
                    logger.error(e)


    @staticmethod
    async def new_buy(sold_items: list[CartItemDTO], user: UserDTO, session: AsyncSession):
        user_button = await NotificationService.make_user_button(user.telegram_username)
        cart_grand_total = 0.0
        message = ""
        for proxy in sold_items:
            price = await ProxiesRepository.get_price(ProxyDTO(country_id=proxy.country_id,
                                                    name=proxy.name, proxy_type_id=proxy.proxy_type_id), session)
            country = await CountryRepository.get_by_id(proxy.country_id, session)
            proxy_type_id = await ProxyTypeRepository.get_by_id(proxy.proxy_type_id, session)
            cart_item_total = float(price) * float(proxy.quantity)
            cart_grand_total += cart_item_total
            if user.telegram_username:
                message += ("🛒 Новая покупка пользователя @{username} на сумму {total_price:.2f} руб. \n"
                            "Количество прокси {quantity} шт. \n Страна: {country_name}. "
                            "Тип прокси: \n {proxy_type}.").format(
                    username=user.telegram_username,
                    total_price=cart_item_total,
                    quantity=proxy.quantity,
                    country_name=country.country_name,
                    proxy_type=proxy_type_id.proxy_type + "\n"
                )
            else:
                message += ("🛒 Новая покупка пользователя с ID {telegram_id} на сумму {total_price:.2f} руб. \n"
                            "Количество прокси {quantity} шт. \n Страна: {country_name}. "
                            "Тип прокси: \n {proxy_type}.").format(
                    telegram_id=user.telegram_id,
                    total_price=cart_item_total,
                    quantity=proxy.quantity,
                    country_name=country.country_name,
                    proxy_type=proxy_type_id.proxy_type + "\n")
        message += "\n<u>Общая сумма: {cart_grand_total:.2f} руб.</u>".format(
            cart_grand_total=cart_grand_total
        )
        await NotificationService.send_to_admins(message, user_button)


