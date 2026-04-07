from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.callbacks import CartCallback, SortingCallback


async def add_pagination_buttons(keyboard_builder: InlineKeyboardBuilder, unpacked_cb, max_page_function,
                                 back_button) -> InlineKeyboardBuilder:
    maximum_page = await max_page_function
    buttons: list[InlineKeyboardButton] = []

    if unpacked_cb.page > 0:
        back_page_callback = unpacked_cb.__copy__()
        back_page_callback.page -= 1
        first_page_callback = unpacked_cb.__copy__()
        first_page_callback.page = 0

        buttons.append(types.InlineKeyboardButton(text="⏪ В начало", callback_data=first_page_callback.pack()))
        buttons.append(types.InlineKeyboardButton(text="⬅️ Пред.", callback_data=back_page_callback.pack()))


    if unpacked_cb.page < maximum_page:
        last_page_callback = unpacked_cb.__copy__()
        last_page_callback.page = maximum_page
        unpacked_cb.page += 1

        buttons.append(types.InlineKeyboardButton(text="➡️ След.", callback_data=unpacked_cb.pack()))
        buttons.append(types.InlineKeyboardButton(text="⏩ Последняя", callback_data=last_page_callback.pack()))

    keyboard_builder.row(*buttons)
    if back_button:
        keyboard_builder.row(back_button)
    return keyboard_builder


async def add_pagination_buttons_for_cart(keyboard_builder: InlineKeyboardBuilder, unpacked_cb,
                                          max_qty, cart_qty,  cart_item_id) -> InlineKeyboardBuilder:
    buttons: list[InlineKeyboardButton] = [
        types.InlineKeyboardButton(text="🗑", callback_data=CartCallback.create(level=2, cart_item_id=cart_item_id).pack())
    ]

    if cart_qty > 1:
        buttons.append(types.InlineKeyboardButton(text="➖1️⃣", callback_data=CartCallback.create(level=1,
                                cart_item_id=cart_item_id ,cart_qty=cart_qty, max_qty=max_qty, action="-").pack()))

    if cart_qty < max_qty:
        buttons.append(types.InlineKeyboardButton(text="➕1️⃣", callback_data=CartCallback.create(level=1,
                                cart_item_id=cart_item_id ,cart_qty=cart_qty, max_qty=max_qty, action="+").pack()))

        buttons.append(types.InlineKeyboardButton(text="♾️", callback_data=CartCallback.create(level=1,
                                cart_item_id=cart_item_id ,cart_qty=cart_qty, max_qty=max_qty, action="♾️").pack()))
    keyboard_builder.row(*buttons)

    return keyboard_builder


# async def get_filters_settings(state: FSMContext,
#                                callback_data: SortingCallback) -> tuple[dict[str, int], list[str]]:
#     state_data = await state.get_data()
#     sort_pairs = state_data.get("sort_pairs", {}).copy()
#     sort_key = str(callback_data.sort_property.value)
#     sort_pairs[sort_key] = callback_data.sort_order.value
#     await state.update_data(sort_pairs=sort_pairs)
#     filter_data = state_data.get("filter")
#     if filter_data is not None:
#         filters = [f.strip() for f in filter_data.split(",")]
#         callback_data.is_filter_enabled = True
#     else:
#         filters = None
#     return sort_pairs, filters



