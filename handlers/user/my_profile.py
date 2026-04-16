from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from services.buy import BuyService
from services.notification import NotificationService
from services.payment import PaymentService
from services.user import UserService
from utils.callbacks import MyProfileCallback

my_profile_router = Router()


@my_profile_router.message(F.text == "Личный кабинет")
async def my_profile_text_message(message: Message, session: AsyncSession, state: FSMContext):
    await my_profile(message=message, session=session, state=state)


async def my_profile(**kwargs):
    message: Message | CallbackQuery = kwargs.get("message") or kwargs.get("callback")
    session: AsyncSession = kwargs.get("session")
    state: FSMContext = kwargs.get("state")
    await state.clear()
    media, kb_builder = await UserService.get_my_profile_buttons(message.from_user.id, session)
    if isinstance(message, Message):
        await NotificationService.answer_media(message, media, kb_builder.as_markup())
    elif isinstance(message, CallbackQuery):
        callback = message
        await callback.message.edit_media(media=media, reply_markup=kb_builder.as_markup())


async def top_up_balance(**kwargs):
    callback: CallbackQuery = kwargs.get("callback")
    callback_data: MyProfileCallback = kwargs.get("callback_data")
    state: FSMContext = kwargs.get("state")
    await state.set_state()
    msg_text, kb_builder = await UserService.get_top_up_buttons(callback_data)
    await callback.message.edit_caption(caption=msg_text, reply_markup=kb_builder.as_markup())


async def create_payment(**kwargs):
    callback: CallbackQuery = kwargs.get("callback")
    session: AsyncSession = kwargs.get("session")
    callback_data: MyProfileCallback = kwargs.get("callback_data")
    state: FSMContext = kwargs.get("state")
    response, kb_builder = await PaymentService.create(callback, callback_data, state, session)
    if isinstance(response, str):
        await callback.message.edit_caption(caption=response, reply_markup=kb_builder.as_markup())
    else:
        await callback.message.edit_media(media=response, reply_markup=kb_builder.as_markup())


async def purchase_history(**kwargs):
    callback: CallbackQuery = kwargs.get("callback")
    callback_data: MyProfileCallback = kwargs.get("callback_data")
    session: AsyncSession = kwargs.get("session")
    msg_text, kb_builder = await UserService.get_purchase_history_buttons(callback.from_user.id, callback_data, session)

    if callback.message.caption:
        await callback.message.edit_caption(caption=msg_text, reply_markup=kb_builder.as_markup())
    else:
        await callback.message.edit_text(text=msg_text, reply_markup=kb_builder.as_markup())


async def get_purchased_item(**kwargs):
    callback: CallbackQuery = kwargs.get("callback")
    callback_data: MyProfileCallback = kwargs.get("callback_data")
    session: AsyncSession = kwargs.get("session")

    msg_text, kb_builder = await BuyService.get_purchased_item(callback_data, session)

    if callback.message.caption:
        await callback.message.edit_caption(caption=msg_text, reply_markup=kb_builder.as_markup())
    else:
        await callback.message.edit_text(text=msg_text, reply_markup=kb_builder.as_markup())


@my_profile_router.callback_query(MyProfileCallback.filter())
async def navigate(callback: CallbackQuery,
                   callback_data: MyProfileCallback,
                   session: AsyncSession,
                   state: FSMContext):
    current_level = callback_data.level

    levels = {
        0: my_profile,
        1: top_up_balance,
        2: create_payment,
        3: purchase_history,
        4: get_purchased_item
    }

    current_level_function = levels[current_level]

    kwargs = {
        "callback": callback,
        "session": session,
        "callback_data": callback_data,
        "state": state,
    }

    await current_level_function(**kwargs)