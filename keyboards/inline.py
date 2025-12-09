from aiogram.filters.callback_data import CallbackData
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


def proxies_kb(proxy_name: str) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=f"{proxy_name}", callback_data=f"name_{proxy_name}"))
    kb.adjust(2)
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
rental_period.adjust(1)


class GlobalData:
    data = {}

    @classmethod
    async def update_data(cls, key, value):
        cls.data[key] = value



