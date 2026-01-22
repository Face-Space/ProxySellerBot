from aiogram.filters.callback_data import CallbackData


class ProxyCatalogCallback(CallbackData, prefix="proxy_catalog"):
    level: int
    # category_id: int
    country: str | None = None
    proxy_type: str | None = None
    period: int | None = None
    quantity: int | None = None
    price: int | None = None


class CartCallback(CallbackData, prefix="cart"):
    page: int
    cart_id: int
    cart_item_id: int
    confirmation: bool




