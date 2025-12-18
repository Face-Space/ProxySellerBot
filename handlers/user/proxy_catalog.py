from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice
from sqlalchemy.ext.asyncio import AsyncSession

import config
from FSM.states import ProxyCatalog
from bot_setup import bot
from keyboards.inline import *
from orm_query.proxies import ProxiesRepository

proxy_catalog_router = Router()


@proxy_catalog_router.message(F.text == "Каталог прокси")
async def get_country(message: types.Message, state: FSMContext):

    # далее работает уже с апи
    # proxy_catalog = ProxyProviderClient("https://api.proxy-provider.com", "your-api-key")
    # proxies = proxy_catalog.fetch_products()

    await message.answer("Вот каталог всех прокси📦 по странам", reply_markup=proxy_loc.as_markup())
    await state.set_state(ProxyCatalog.country)


@proxy_catalog_router.callback_query(F.data.startswith("country"), ProxyCatalog.country)
async def get_type(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    country_name = callback.data.split("_")[1]

    # сохраняем полученный коллбэк в словарь, который потом используем для запроса
    await state.update_data(country_name=country_name)
    await callback.message.answer("Выберите интересующий вас тип прокси:", reply_markup=type_proxy.as_markup())
    await state.set_state(ProxyCatalog.proxy_type)


@proxy_catalog_router.callback_query(F.data.startswith("type"), ProxyCatalog.proxy_type)
async def get_period(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    proxy_type = callback.data.split("_")[1]
    await state.update_data(proxy_type=proxy_type)
    await callback.message.answer("Отлично, теперь укажите желаемый срок аренды прокси:",
                                  reply_markup=rental_period.as_markup())
    await state.set_state(ProxyCatalog.period)


@proxy_catalog_router.callback_query(F.data.startswith("period"))
async def get_prox(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    await callback.answer()
    period_days = callback.data.split("_")[1]
    await state.update_data(period_days=period_days)

    await state.get_data()
    data = await ProxiesRepository.get_proxy(session, GlobalData.data)
    print(data)
    await callback.message.answer("Вот все доступные прокси под ваши параметры:",
                                  reply_markup=proxies_kb(data).as_markup())



@proxy_catalog_router.callback_query(F.data.startswith("name"))
async def get_proxies_quantity(callback: types.CallbackQuery, session: AsyncSession):
    await callback.answer()
    quantity = callback.data.split("_")[1]
    price = callback.data.split("_")[2]
    await GlobalData.update_data("price", price)
    await callback.message.answer(f"Выберите необходимое количество прокси из доступно возможных:",
                                  reply_markup=proxy_quantity(int(quantity)).as_markup())


@proxy_catalog_router.callback_query(F.data.startswith("quantity"))
async def payment(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Выберите способ оплаты:", reply_markup=payment_types.as_markup())


@proxy_catalog_router.callback_query(F.data.startswith("payment"))
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