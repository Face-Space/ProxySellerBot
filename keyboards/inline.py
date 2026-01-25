from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.callbacks import ProxyCatalogCallback


proxy_loc = InlineKeyboardBuilder()
countries = {"Канада":"🇨🇦", "США":"🇺🇸", "Польша":"🇵🇱", "Финляндия":"🇫🇮", "Латвия":"🇱🇻", "Россия":"🇷🇺"}
for nation, flag in countries.items():
    proxy_loc.add(InlineKeyboardButton(text=f"{nation+flag}",
                                       callback_data=ProxyCatalogCallback(level=1, country=f"{nation}").pack()))

proxy_loc.adjust(2)


def type_proxy(callback: CallbackQuery):
    unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
    country = unpacked_cb.country
    kb = InlineKeyboardBuilder()
    proxies_types = ["HTTP", "HTTPS", "SOCKS5"]
    for p in proxies_types:
        kb.add(InlineKeyboardButton(text=f"{p}",
                callback_data=ProxyCatalogCallback(level=2, country=country, proxy_type=f"{p}").pack()))

    kb.add(InlineKeyboardButton(text=f"Назад", callback_data=ProxyCatalogCallback(level=0).pack()))
    kb.adjust(2)
    return kb


def rental_period(callback: CallbackQuery):
    unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
    country = unpacked_cb.country
    proxy_type = unpacked_cb.proxy_type
    kb = InlineKeyboardBuilder()
    periods = {
        "1 день": "1",
        "7 дней": "7",
        "1 месяц": "30",
        "6 месяцев": "180",
        "1 год": "365"
    }
    for day, cb in periods.items():
        kb.add(InlineKeyboardButton(text=day, callback_data=ProxyCatalogCallback(
            level=3, country=country, proxy_type=proxy_type, period=int(cb)).pack())
        )
    kb.add(InlineKeyboardButton(text=f"Назад", callback_data=ProxyCatalogCallback(level=1, country=country).pack()))
    kb.adjust(2)
    return kb


def proxies_kb(callback: CallbackQuery, data: dict) -> InlineKeyboardBuilder:
    unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
    kb = InlineKeyboardBuilder()
    country = unpacked_cb.country
    proxy_type = unpacked_cb.proxy_type
    period = unpacked_cb.period

    for proxy in data:
        proxy_name = proxy.name
        quantity = proxy.quantity
        price = proxy.price

        kb.add(InlineKeyboardButton(text=f"{proxy_name}", callback_data=ProxyCatalogCallback(
            level=4,
            name=proxy_name,
            country=country,
            proxy_type=proxy_type,
            period=period,
            quantity=quantity,
            price=price).pack())
        )
    kb.add(InlineKeyboardButton(text=f"Назад",
                    callback_data=ProxyCatalogCallback(level=2, country=country, proxy_type=proxy_type).pack()))
    kb.adjust(1)
    return kb


def proxy_quantity(callback: CallbackQuery) -> InlineKeyboardBuilder:
    unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
    name = unpacked_cb.name
    price = unpacked_cb.price
    country = unpacked_cb.country
    proxy_type = unpacked_cb.proxy_type
    period = unpacked_cb.period
    quantity = unpacked_cb.quantity

    kb = InlineKeyboardBuilder()
    for i in range(quantity):
        kb.add(InlineKeyboardButton(text=f"{i+1}",
            callback_data=ProxyCatalogCallback(
                level=5,
                name=name,
                country=country,
                proxy_type=proxy_type,
                period=period,
                price=price,
                quantity=i+1).pack()))

    kb.add(InlineKeyboardButton(text=f"Назад",
                                callback_data=ProxyCatalogCallback(level=3, country=country,
                                                                   proxy_type=proxy_type, price=price).pack()))
    kb.adjust(2)
    return kb


payment_types = InlineKeyboardBuilder()
payment_types.add(InlineKeyboardButton(text="Paymaster", callback_data="payment_paymaster"),
                  InlineKeyboardButton(text="USDT", callback_data="payment_usdt"))
payment_types.adjust(2)


def confirm_payment(pay_url: str):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить USDT", url=pay_url)]
    ])
    return kb
