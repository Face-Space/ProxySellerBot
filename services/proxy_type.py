from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from orm_query.proxy_type import ProxyTypeRepository
from utils.callbacks import ProxyCatalogCallback


class ProxyTypeService:

    @staticmethod
    async def get_buttons(callback: CallbackQuery, session: AsyncSession) -> tuple[str, InlineKeyboardBuilder]:
        unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
        kb_builder = InlineKeyboardBuilder()
        proxy_types = await ProxyTypeRepository.get_paginated_by_country_id(unpacked_cb.country_id,
                                                                             unpacked_cb.page, session)

        for proxy_type in proxy_types:


