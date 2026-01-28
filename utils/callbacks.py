from aiogram import types
from aiogram.filters.callback_data import CallbackData


class BaseCallback(CallbackData, prefix="base"):
    level: int

    def get_back_button(self, lvl: int | None = None):
        cb_copy = self.__copy__()
        if lvl is None:
            cb_copy.level = cb_copy.level - 1
        else:
            cb_copy.level = lvl

        return types.InlineKeyboardButton(text="Назад", callback_data=cb_copy.create(**cb_copy.model_dump()).pack())


class ProxyCatalogCallback(BaseCallback, prefix="proxy_catalog"):
    country_id: int
    period: int
    quantity: int
    price: float
    confirmation: bool
    page: int

    @staticmethod
    def create(level: int,
               country_id: int = -1,
               period: int = 0,
               quantity: int = 0,
               price: float = 0.0,
               confirmation: bool = False,
               page: int = 0) -> 'ProxyCatalogCallback':
        return ProxyCatalogCallback(level=level, country_id=country_id, period=period, quantity=quantity, price=price,
                                    confirmation=confirmation, page=page)




class CartCallback(BaseCallback, prefix="cart"):
    page: int
    cart_id: int
    cart_item_id: int
    confirmation: bool




