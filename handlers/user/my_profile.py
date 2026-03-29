from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from services.user import UserService

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


