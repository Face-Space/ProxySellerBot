from datetime import date

from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
import logging

from aiogram.types import PreCheckoutQuery
from sqlalchemy.ext.asyncio import AsyncSession

import config
from keyboards.reply import start_kb
from models.user import UserDTO
from services.user import UserService

logger = logging.getLogger(__name__)
user_router = Router()



@user_router.message(CommandStart())
async def start_bot(message: types.Message, session: AsyncSession):
    await message.answer("Привет👋, я ProxySellerBot🤖, и я помогу тебе выбрать необходимый для тебя прокси!",
                         reply_markup=start_kb)

    await UserService.create_if_not_exist(UserDTO(
        telegram_username=message.from_user.username,
        telegram_id=message.from_user.id
    ), session)
    # безопасное извлечения/валидация пользовательских данных из сессии БД перед обработкой сообщений


# Перед оплатой Telegram вызывает этот обработчик
@user_router.pre_checkout_query()
async def pre_checkout_q(message: types.Message, pre_checkout_query: PreCheckoutQuery):
    bot = message.bot
    try:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    except Exception as e:
        logger.error(f"Ошибка оплаты: {e}")
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False, error_message=f"Ошибка оплаты ❌:{e}.\n\n "
                                "Недостаточно средств на счету либо проверьте правильность введённых данных.")


# Успешная оплата — Telegram отправляет ContentType.SUCCESSFUL_PAYMENT
@user_router.message(F.successful_payment)
async def successful_payment(message: types.Message, session: AsyncSession):
    try:
        sub_interval = UserService.parse_interval(message.successful_payment.invoice_payload)
        end_subscription = date.today() + sub_interval
        # await orm_mark_user_paid(session, message.from_user.id, end_subscription)
        await message.answer("Спасибо за оплату! ☺️️\nВот ваш прокси: ✅. \n")

    except Exception as e:
        logger.error(f"Ошибка оплаты: {e}")
        await message.answer(f"Ошибка на стороне сервера  ❌:{e}. Пожалуйста попробуйте позже 😞")


@user_router.message(~Command("admin"))
async def delete_trash(message: types.Message):
    await message.delete()


