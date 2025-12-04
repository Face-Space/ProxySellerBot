from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Каталог прокси"),
        KeyboardButton(text="Личный кабинет")
     ],
    [
        KeyboardButton(text="Корзина"),
        KeyboardButton(text="Связь с админом")
    ]
], resize_keyboard=True)




