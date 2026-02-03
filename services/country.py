from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from orm_query.country import CountryRepository
from utils.callbacks import ProxyCatalogCallback
from utils.common import add_pagination_buttons


class CountryService:

    @staticmethod
    async def get_buttons(session: AsyncSession, callback: CallbackQuery | None = None) -> tuple[str, InlineKeyboardBuilder]:
        if callback is None:
            unpacked_cb = ProxyCatalogCallback.create(0)
        else:
            unpacked_cb = ProxyCatalogCallback.unpack(callback.data)

        countries = await CountryRepository.get(unpacked_cb.page, session)
        country_builder = InlineKeyboardBuilder()
        [country_builder.button(text=f"{country.country_name}{country.country_flag}",
            callback_data=ProxyCatalogCallback.create(level=1, country_id=country.id)) for country in countries]
        country_builder.adjust(2)
        country_builder = await add_pagination_buttons(country_builder, unpacked_cb,
                                                       CountryRepository.get_maximum_page(session), None)

        if len(country_builder.as_markup().inline_keyboard) == 0:
            return "Извините, все прокси распроданы😔", country_builder
        else:
            return "Вот каталог всех прокси📦 по странам", country_builder




