from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from orm_query.country import CountryRepository
from orm_query.period import PeriodRepository
from orm_query.proxies import ProxiesRepository
from orm_query.proxy_type import ProxyTypeRepository
from utils.callbacks import ProxyCatalogCallback
from utils.common import add_pagination_buttons


class ProxyService:

    @staticmethod
    async def get_buttons(callback: CallbackQuery, session: AsyncSession) -> tuple[str, InlineKeyboardBuilder]:
        unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
        kb_builder = InlineKeyboardBuilder()
        proxy_types = await ProxyTypeRepository.get_paginated_by_country_id(unpacked_cb.country_id,
                                                                             unpacked_cb.page, session)
        for proxy_type in proxy_types:
            kb_builder.button(text="{proxy_type}".format(
                proxy_type=proxy_type.proxy_type),
                callback_data=ProxyCatalogCallback.create(
                unpacked_cb.level + 1,
                country_id=unpacked_cb.country_id,
                proxy_type_id=proxy_type.id
            ))
        kb_builder.adjust(1)
        kb_builder = await add_pagination_buttons(kb_builder, unpacked_cb,
                                                ProxyTypeRepository.max_page(unpacked_cb.country_id, session),
                                                unpacked_cb.get_back_button())

        return "📦 Выберите интересующий вас тип прокси:", kb_builder


    @staticmethod
    async def show_filtered_proxies(callback: CallbackQuery, session: AsyncSession) -> tuple[str, InlineKeyboardBuilder]:
        unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
        kb_builder = InlineKeyboardBuilder()
        proxies = await ProxiesRepository.get_available_proxies(unpacked_cb.country_id, unpacked_cb.proxy_type_id, session)

        for proxy in proxies:
            kb_builder.button(text=f"📦 {proxy.name}| Цена: {proxy.price:.2f} руб. за 1шт.",
                              callback_data=ProxyCatalogCallback.create(
                                  unpacked_cb.level + 1,
                                  proxy.name,
                                  unpacked_cb.country_id,
                                  proxy.proxy_type_id
                              ))
        kb_builder.adjust(1)
        kb_builder.row(unpacked_cb.get_back_button())
        return "📦 Вот все доступные прокси по вашему запросу:", kb_builder


    @staticmethod
    async def get_select_quantity_buttons(callback: CallbackQuery, session: AsyncSession) -> tuple[str, InlineKeyboardBuilder]:
        unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
        proxy = await ProxiesRepository.get_single(unpacked_cb.country_id, unpacked_cb.proxy_type_id,
                                                   unpacked_cb.proxy_name, session)
        proxy_type = await ProxyTypeRepository.get_by_id(unpacked_cb.proxy_type_id, session)
        country = await CountryRepository.get_by_id(unpacked_cb.country_id, session)
        kb_builder = InlineKeyboardBuilder()
        available_qty = await ProxiesRepository.get_available_qty(proxy, session)

        if available_qty is None:
            return "Извините, но этот прокси уже был продан😔", kb_builder


        message_text = ("🛒 <b>Название прокси: {proxy_name}\nСтрана: {country_name}{flag}\nТип прокси: {proxy_type}\n"
                        "💰 Цена: {price:.2f} {currency_sym}\nДоступное количество: {quantity}\n"
                        "Выберите необходимое для вас количество прокси из доступно возможных:</b>").format(
            proxy_name=unpacked_cb.proxy_name,
            country_name=country.country_name,
            flag=country.country_flag,
            proxy_type=proxy_type.proxy_type,
            price=proxy.price,
            quantity=available_qty,
            currency_sym="руб."
        )

        for i in range(available_qty):
            kb_builder.button(text=str(i+1), callback_data=ProxyCatalogCallback.create(
                unpacked_cb.level + 1,
                unpacked_cb.proxy_name,
                proxy.country_id,
                proxy.proxy_type_id,
                quantity=i+1
            ))
        kb_builder.adjust(3)
        kb_builder.row(unpacked_cb.get_back_button())

        return message_text, kb_builder



    @staticmethod
    async def get_select_period_buttons(callback: CallbackQuery, session: AsyncSession) -> tuple[str, InlineKeyboardBuilder]:
        unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
        proxy = await ProxiesRepository.get_single(unpacked_cb.country_id, unpacked_cb.proxy_type_id,
                                                   unpacked_cb.proxy_name, session)
        periods = await PeriodRepository.get_all_periods(session)
        available_qty = await ProxiesRepository.get_available_qty(proxy, session)
        kb_builder = InlineKeyboardBuilder()

        if available_qty is None:
            return "Извините, но этот прокси уже был продан😔", kb_builder

        [kb_builder.button(text=f"{str(period.period_days)}",
                           callback_data=ProxyCatalogCallback.create(
                               unpacked_cb.level + 1,
                               unpacked_cb.proxy_name,
                               proxy.country_id,
                               proxy.proxy_type_id,
                               quantity=unpacked_cb.quantity,
                               period=period.period_days)) for period in periods]

        kb_builder.adjust(2)
        kb_builder.row(unpacked_cb.get_back_button())
        return "🕐 Выберите период на который вы хотите арендовать прокси:", kb_builder


    @staticmethod
    async def get_add_to_cart_buttons(callback: CallbackQuery, session: AsyncSession) -> tuple[str, InlineKeyboardBuilder]:
        unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
        proxy = await ProxiesRepository.get_single(unpacked_cb.country_id, unpacked_cb.proxy_type_id,
                                                   unpacked_cb.proxy_name, session)
        proxy_type = await ProxyTypeRepository.get_by_id(unpacked_cb.proxy_type_id, session)
        country = await CountryRepository.get_by_id(unpacked_cb.country_id, session)
        available_qty = await ProxiesRepository.get_available_qty(proxy, session)
        kb_builder = InlineKeyboardBuilder()

        if available_qty is None:
            return "Извините, но этот прокси уже был продан😔", kb_builder

        message_text = ("🛒 <b>Название прокси: {proxy_name} Страна: {country_name}{flag}\nТип прокси: {proxy_type}"
                        "\nЦена: {price} {currency_sym}\nВыбранное количество прокси: {quantity}\n"
                        "💰 Итоговая сумма: {total_price} {currency_sym}</b>").format(
            proxy_name=proxy.name,
            country_name=country.country_name,
            flag=country.country_flag,
            proxy_type=proxy_type.proxy_type,
            price=proxy.price,
            quantity=unpacked_cb.quantity,
            total_price=proxy.price * unpacked_cb.quantity,
            currency_sym="руб."
        )
        kb_builder.button(text="✅ Подтвердить",
                          callback_data=ProxyCatalogCallback.create(
                              unpacked_cb.level + 1,
                              unpacked_cb.proxy_name,
                              unpacked_cb.country_id,
                              unpacked_cb.proxy_type_id,
                              unpacked_cb.period,
                              unpacked_cb.quantity,
                              confirmation=True
                          ))
        kb_builder.button(text="❌ Отмена",
                          callback_data=ProxyCatalogCallback.create(
                              1,
                              country_id=unpacked_cb.country_id
                          ))
        kb_builder.row(unpacked_cb.get_back_button())
        return message_text, kb_builder




