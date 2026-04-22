from aiogram import types
from aiogram.filters.callback_data import CallbackData

from enums.cryptocurrency import Cryptocurrency
from enums.sort_order import SortOrder
from enums.sort_property import SortProperty
from enums.user_role import UserRole


class BaseCallback(CallbackData, prefix="base"):
    level: int
    page: int = 0

    def get_back_button(self, lvl: int | None = None):
        cb_copy = self.__copy__()
        if lvl is None:
            cb_copy.level = cb_copy.level - 1
        else:
            cb_copy.level = lvl

        return types.InlineKeyboardButton(text="⬅️ Назад", callback_data=cb_copy.create(**cb_copy.model_dump()).pack())

class SortingCallback(CallbackData, prefix="sorting"):
    sort_order: SortOrder
    sort_property: SortProperty
    is_filter_enabled: bool = False


class ProxyCatalogCallback(BaseCallback, prefix="proxy_catalog"):
    proxy_name: str | None
    country_id: int
    proxy_type_id: int
    period: str | None
    quantity: int
    price: float
    confirmation: bool


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
    cart_id: int
    cart_item_id: int
    confirmation: bool
    max_qty: int | None
    cart_qty: int | None
    action: str | None
    cart_grand_total: int | None

    @staticmethod
    def create(level: int = 0, page: int = 0, cart_id: int = -1, cart_item_id: int = -1, max_qty: int | None = None,
               cart_qty: int | None = None, confirmation=False, action: str | None = None, cart_grand_total: int | None = None):
        return CartCallback(level=level, page=page, cart_id=cart_id, cart_item_id=cart_item_id, max_qty=max_qty,
                            cart_qty=cart_qty, confirmation=confirmation, action=action, cart_grand_total=cart_grand_total)


class MyProfileCallback(BaseCallback, SortingCallback, prefix="my_profile"):
    buy_id: int | None = None
    buyItem_id: int | None = None
    cryptocurrency: Cryptocurrency | None = None
    user_role: UserRole = UserRole.USER
    confirmation: bool = False

    @staticmethod
    def create(level: int,
               buy_id: int | None = None,
               buyItem_id: int | None = None,
               sort_order: SortOrder = SortOrder.DISABLE,
               sort_property: SortProperty = SortProperty.BUY_DATETIME,
               is_filter_enabled: bool = False,
               cryptocurrency: Cryptocurrency | None = None,
               user_role: UserRole = UserRole.USER,
               confirmation: bool = False,
               page=0) -> 'MyProfileCallback':
        return MyProfileCallback(level=level, buy_id=buy_id, buyItem_id=buyItem_id,
                                 sort_order=sort_order, sort_property=sort_property,
                                 is_filter_enabled=is_filter_enabled,
                                 cryptocurrency=cryptocurrency,
                                 user_role=user_role,
                                 confirmation=confirmation,
                                 page=page)


class AdminMenuCallback(BaseCallback, prefix="admin_menu"):

    @staticmethod
    def create(level: int, page: int = 0):
        return AdminMenuCallback(level=level, page=page)


