from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



proxy_loc = InlineKeyboardBuilder()
proxy_loc.add(InlineKeyboardButton(text="Канада🇨🇦", callback_data="страна_Канада🇨🇦"),
              InlineKeyboardButton(text="США🇺🇸", callback_data="страна_США🇺🇸"),
              InlineKeyboardButton(text="Польша🇵🇱", callback_data="страна_Польша🇵🇱"),
              InlineKeyboardButton(text="Финляндия🇫🇮", callback_data="страна_Финляндия🇫🇮"),
              InlineKeyboardButton(text="Латвия🇱🇻", callback_data="страна_Латвия🇱🇻"),
              InlineKeyboardButton(text="Россия🇷🇺", callback_data="страна_Россия🇷🇺"))
proxy_loc.adjust(2)


def proxies_kb(proxy_name: str) -> InlineKeyboardBuilder:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text=f"{proxy_name}"))
    kb.adjust(2)
    return kb

