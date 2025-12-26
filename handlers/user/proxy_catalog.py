# from aiogram import Router, F, types
# from aiogram.filters import StateFilter
# from aiogram.fsm.context import FSMContext
# from aiogram.types import LabeledPrice
# from sqlalchemy.ext.asyncio import AsyncSession
#
# import config
# from FSM.states import ProxyCatalog
# from bot_setup import bot
# from keyboards.inline import *
# from models.user import UserDTO
# from orm_query.proxies import ProxiesRepository
# from services.crypto_pay_client import CryptoPayClient
# from services.user import UserService
#
# proxy_catalog_router = Router()
# cp = CryptoPayClient(config.CRYPTO_PAY_TOKEN)
#
#
# @proxy_catalog_router.message(F.text == "Каталог прокси")
# async def get_country(message: types.Message, state: FSMContext):
#
#     # далее работает уже с апи
#     # proxy_catalog = ProxyProviderClient("https://api.proxy-provider.com", "your-api-key")
#     # proxies = proxy_catalog.fetch_products()
#
#     await state.clear()
#     await message.answer("Вот каталог всех прокси📦 по странам", reply_markup=proxy_loc.as_markup())
#     await state.set_state(ProxyCatalog.country)
#
#
# @proxy_catalog_router.callback_query(F.data.startswith("country"), ProxyCatalog.country)
# async def get_type(callback: types.CallbackQuery, state: FSMContext):
#     await callback.answer()
#     country_name = callback.data.split("_")[1]
#
#     # сохраняем полученный коллбэк в словарь, который потом используем для запроса
#     await state.update_data(country_name=country_name)
#     await callback.message.answer("Выберите интересующий вас тип прокси:", reply_markup=type_proxy.as_markup())
#     await state.set_state(ProxyCatalog.proxy_type)
#
#
# @proxy_catalog_router.callback_query(F.data.startswith("type"), ProxyCatalog.proxy_type)
# async def get_period(callback: types.CallbackQuery, state: FSMContext):
#     await callback.answer()
#     proxy_type = callback.data.split("_")[1]
#     await state.update_data(proxy_type=proxy_type)
#     await callback.message.answer("Отлично, теперь укажите желаемый срок аренды прокси:",
#                                   reply_markup=rental_period.as_markup())
#     await state.set_state(ProxyCatalog.period)
#
#
# @proxy_catalog_router.callback_query(F.data.startswith("period"), ProxyCatalog.period)
# async def get_prox(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):
#     await callback.answer()
#     period_days = callback.data.split("_")[1]
#     await state.update_data(period_days=period_days)
#
#     data = await state.get_data()
#     db_data = await ProxiesRepository.get_proxy(session, data)
#
#     if db_data is None:
#         await callback.message.answer('Извините, прокси под ваши запросы не найдены. '
#                                       'Нажмите "Каталог прокси" чтобы найти что-нибудь другое')
#         await state.clear()
#     else:
#         await callback.message.answer("Вот все доступные прокси под ваши параметры:",
#                                       reply_markup=proxies_kb(db_data).as_markup())
#     await state.set_state(ProxyCatalog.get_prox)
#
#
# @proxy_catalog_router.callback_query(F.data.startswith("name"), ProxyCatalog.get_prox)
# async def get_proxies_quantity(callback: types.CallbackQuery, state: FSMContext):
#     await callback.answer()
#     quantity = callback.data.split("_")[1]
#     price = callback.data.split("_")[2]
#     await state.update_data(price=price)
#     await callback.message.answer(f"Выберите необходимое количество прокси из доступно возможных:",
#                                   reply_markup=proxy_quantity(int(quantity)).as_markup())
#     await state.set_state(ProxyCatalog.proxies_quantity)
#
#
# @proxy_catalog_router.callback_query(ProxyCatalog.proxies_quantity)
# async def add_to_cart(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
#     await callback.answer()
#     telegram_id = callback.from_user.id
#     await UserService.create_if_not_exist(UserDTO(
#         telegram_username=callback.from_user.username,
#         telegram_id=telegram_id
#     ), session)
#     # чекаем есть ли юзер в БД и если нет то создаём корзину, если да - то обновляем данные
#
#     await callback.message.answer("Товар добавлен в корзину")
#     await state.clear()
#
