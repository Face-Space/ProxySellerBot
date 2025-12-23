from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



proxy_loc = InlineKeyboardBuilder()
proxy_loc.add(InlineKeyboardButton(text="Канада🇨🇦", callback_data="country_Канада"),
              InlineKeyboardButton(text="США🇺🇸", callback_data="country_США"),
              InlineKeyboardButton(text="Польша🇵🇱", callback_data="country_Польша"),
              InlineKeyboardButton(text="Финляндия🇫🇮", callback_data="country_Финляндия"),
              InlineKeyboardButton(text="Латвия🇱🇻", callback_data="country_Латвия"),
              InlineKeyboardButton(text="Россия🇷🇺", callback_data="country_Россия"))
proxy_loc.adjust(2)


def proxies_kb(data: dict) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    for proxy in data:
        proxy_name = proxy.name
        quantity = proxy.quantity
        price = proxy.price
        kb.add(InlineKeyboardButton(text=f"{proxy_name}", callback_data=f"name_{quantity}_{price}"))
    kb.adjust(1)
    return kb


type_proxy = InlineKeyboardBuilder()
type_proxy.add(InlineKeyboardButton(text="HTTP/S", callback_data="type_HTTP/S"),
               InlineKeyboardButton(text="SOCKS5", callback_data="type_SOCKS5"),
               InlineKeyboardButton(text="IPv4", callback_data="type_IPv4"))
type_proxy.adjust(1)


rental_period = InlineKeyboardBuilder()
rental_period.add(InlineKeyboardButton(text="1 день", callback_data="period_1"),
                  InlineKeyboardButton(text="7 дней", callback_data="period_7"),
                  InlineKeyboardButton(text="1 месяц", callback_data="period_30"),
                  InlineKeyboardButton(text="6 месяцев", callback_data="period_180"),
                  InlineKeyboardButton(text="1 год", callback_data="period_365"))
rental_period.adjust(2)


# class GlobalData:
#     data = {}
#
#     @classmethod
#     async def update_data(cls, key, value):
#         cls.data[key] = value


def proxy_quantity(quantity: int) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    for i in range(quantity):
        kb.add(InlineKeyboardButton(text=f"{i+1}", callback_data=f"quantity_{i+1}"))
    kb.adjust(2)
    return kb


payment_types = InlineKeyboardBuilder()
payment_types.add(InlineKeyboardButton(text="Paymaster", callback_data="payment_paymaster"),
                  InlineKeyboardButton(text="USDT", callback_data="payment_usdt"))
payment_types.adjust(2)

