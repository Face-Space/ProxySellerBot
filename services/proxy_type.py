from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from models.proxies import ProxyDTO
from orm_query.country import CountryRepository
from orm_query.proxies import ProxiesRepository
from orm_query.proxy_type import ProxyTypeRepository
from utils.callbacks import ProxyCatalogCallback
from utils.common import add_pagination_buttons


class ProxyTypeService:

    @staticmethod
    async def get_buttons(callback: CallbackQuery, session: AsyncSession) -> tuple[str, InlineKeyboardBuilder]:
        unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
        kb_builder = InlineKeyboardBuilder()
        proxy_types = await ProxyTypeRepository.get_paginated_by_country_id(unpacked_cb.country_id,
                                                                             unpacked_cb.page, session)

        for proxy_type in proxy_types:
            proxy = await ProxiesRepository.get_single(unpacked_cb.country_id, proxy_type.id, session)
            available_qty = await ProxiesRepository.get_available_qty(ProxyDTO(country_id=unpacked_cb.country_id,
                                                                    proxy_type_id=proxy_type.id), session)
            kb_builder.button(text="📦 {proxy_type}| Цена: {proxy_price:.2f} {currency_sym} за 1шт.".format(
                proxy_type=proxy_type.proxy_type,
                currency_sym="RUB",
                proxy_price=proxy.price,
                available_quantity=available_qty),
                callback_data=ProxyCatalogCallback.create(
                    unpacked_cb.level + 1,
                    unpacked_cb.country_id,
                    proxy_type.id
                )
            )
        kb_builder.adjust(1)
        kb_builder = await add_pagination_buttons(kb_builder, unpacked_cb,
                                                ProxyTypeRepository.max_page(unpacked_cb.country_id, session),
                                                unpacked_cb.get_back_button())

        return "📦 Выберите интересующий вас тип прокси:", kb_builder


    @staticmethod
    async def get_select_quantity_buttons(callback: CallbackQuery, session: AsyncSession) -> tuple[str, InlineKeyboardBuilder]:
        unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
        proxy = await ProxiesRepository.get_single(unpacked_cb.country_id, unpacked_cb.proxy_type_id, session)
        proxy_type = await ProxyTypeRepository.get_by_id(unpacked_cb.proxy_type_id, session)
        country = await CountryRepository.get_by_id(unpacked_cb.country_id, session)
        available_qty = await ProxiesRepository.get_available_qty(proxy, session)

        message_text = ("🛒 <b>Страна: {country_name}\n Тип прокси: {proxy_type}\nPrice: "
                        "{price:.2f} {currency_sym}\nДоступное количество: {quantity}</b>")
                        .format()









