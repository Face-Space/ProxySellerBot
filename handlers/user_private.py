from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
import logging

from aiogram.types import LabeledPrice
from sqlalchemy.ext.asyncio import AsyncSession

import config
from bot_setup import bot
from database.orm_query import get_proxy, get_quantity
from keyboards.inline import proxy_loc, proxies_kb, type_proxy, rental_period, GlobalData, proxy_quantity, payment_types
from keyboards.reply import start_kb
from models.user import UserDTO

logger = logging.getLogger(__name__)
user_router = Router()


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

@user_router.message(F.text == "Каталог прокси")
async def get_country(message: types.Message):

    # далее работает уже с апи
    # proxy_catalog = ProxyProviderClient("https://api.proxy-provider.com", "your-api-key")
    # proxies = proxy_catalog.fetch_products()

    await message.answer("Вот каталог всех прокси📦 по странам", reply_markup=proxy_loc.as_markup())


@user_router.callback_query(F.data.startswith("country"))
async def get_type(callback: types.CallbackQuery):
    await callback.answer()
    country_name = callback.data.split("_")[1]

    # сохраняем полученный коллбэк в словарь, который потом используем для запроса
    await GlobalData.update_data("country_name", country_name)
    await callback.message.answer("Выберите интересующий вас тип прокси:", reply_markup=type_proxy.as_markup())


@user_router.callback_query(F.data.startswith("type"))
async def get_period(callback: types.CallbackQuery):
    await callback.answer()
    proxy_type = callback.data.split("_")[1]
    await GlobalData.update_data("proxy_type", proxy_type)
    await callback.message.answer("Отлично, теперь укажите желаемый срок аренды прокси:", reply_markup=rental_period.as_markup())


@user_router.callback_query(F.data.startswith("period"))
async def get_prox(callback: types.CallbackQuery, session: AsyncSession):
    await callback.answer()
    period_days = callback.data.split("_")[1]
    await GlobalData.update_data("period_days", period_days)

    data = await get_proxy(session, GlobalData.data)
    print(data)
    await callback.message.answer("Вот все доступные прокси под ваши параметры:",
                                  reply_markup=proxies_kb(data).as_markup())



@user_router.callback_query(F.data.startswith("name"))
async def get_proxies_quantity(callback: types.CallbackQuery, session: AsyncSession):
    await callback.answer()
    quantity = callback.data.split("_")[1]
    price = callback.data.split("_")[2]
    await GlobalData.update_data("price", price)
    await callback.message.answer(f"Выберите необходимое количество прокси из доступно возможных:",
                                  reply_markup=proxy_quantity(int(quantity)).as_markup())


@user_router.callback_query(F.data.startswith("quantity"))
async def get_quantity(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Выберите способ оплаты:", reply_markup=payment_types.as_markup())


@user_router.callback_query(F.data.startswith("payment"))
async def payment(callback: types.CallbackQuery):
    await callback.answer()
    period_days = await GlobalData.data["period_days"]
    price = await GlobalData.data["price"]

    await bot.send_invoice(
        callback.message.chat.id,
        title=f"Покупка прокси на {period_days} дней",
        description="Покупка прокси",
        provider_token=config.PAYMENT_TOKEN,
        currency="rub",
        prices=[LabeledPrice(label=f"Покупка прокси на {period_days}", amount=int(price) * 100)],
        start_parameter="subscription",
        payload=f"{period_days}"
    )


@user_router.message(~Command("admin"))
async def delete_trash(message: types.Message):
    await message.delete()


