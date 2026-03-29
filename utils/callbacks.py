from aiogram import types
from aiogram.filters.callback_data import CallbackData

from enums.sort_order import SortOrder


class BaseCallback(CallbackData, prefix="base"):
    level: int

    def get_back_button(self, lvl: int | None = None):
        cb_copy = self.__copy__()
        if lvl is None:
            cb_copy.level = cb_copy.level - 1
        else:
            cb_copy.level = lvl

        return types.InlineKeyboardButton(text="⬅️ Назад", callback_data=cb_copy.create(**cb_copy.model_dump()).pack())

class SortingCallback(CallbackData, prefix="sorting"):
    sort_order: SortOrder



class ProxyCatalogCallback(BaseCallback, prefix="proxy_catalog"):
    proxy_name: str | None
    country_id: int
    proxy_type_id: int
    period: str | None
    quantity: int
    price: float
    confirmation: bool
    page: int

    @staticmethod
    def create(level: int,
               proxy_name: str = None,
               country_id: int = -1,
               proxy_type_id: int = -1,
               period: str = None,
               quantity: int = 0,
               price: float = 0.0,
               confirmation: bool = False,
               page: int = 0) -> 'ProxyCatalogCallback':
        return ProxyCatalogCallback(level=level, proxy_name=proxy_name, country_id=country_id, proxy_type_id=proxy_type_id,
                                    period=period, quantity=quantity, price=price,
                                    confirmation=confirmation, page=page)


class CartCallback(BaseCallback, prefix="cart"):
    page: int
    cart_id: int
    cart_item_id: int
    confirmation: bool
    max_qty: int | None
    cart_qty: int | None
    action: str | None

    @staticmethod
    def create(level: int = 0, page: int = 0, cart_id: int = -1, cart_item_id: int = -1, max_qty: int | None = None,
               cart_qty: int | None = None, confirmation=False, action: str | None = None):
        return CartCallback(level=level, page=page, cart_id=cart_id, cart_item_id=cart_item_id, max_qty=max_qty,
                            cart_qty=cart_qty, confirmation=confirmation, action=action)

class MyProfileCalback(BaseCallback, SortingCallback, prefix="my_profile")