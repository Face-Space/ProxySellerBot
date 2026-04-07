from datetime import timedelta

from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAnimation
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from enums.cryptocurrency import Cryptocurrency
from enums.keyboard_button import KeyboardButton
from enums.user_role import UserRole
from models.user import UserDTO
from orm_query.button_media import ButtonMediaRepository
from orm_query.buy import BuyRepository
from orm_query.user import UserRepository
from orm_query.cart import CartRepository
from services.media import MediaService
from utils.callbacks import MyProfileCallback, AdminMenuCallback


class UserService:

    @staticmethod
    async def create_if_not_exist(user_dto: UserDTO, session: AsyncSession) -> None:
        user = await UserRepository.get_by_tgid(user_dto.telegram_id, session)
        match user:
            case None:
                user_id = await UserRepository.create(user_dto, session)
                await CartRepository.get_or_create(user_id, session)
                await session.commit()
            case _:
                # update_user_dto = UserDTO(**user.model_dump())
                update_user_dto = UserDTO.model_validate(user, from_attributes=True)
                # при конвертации из ORM-модели в DTO лучше всего использовать model_validate(), а при преобразовании
                # из DTO в ORM лучше использовать model_dump()

                # Без from_attributes=True Pydantic ожидает именно dict-структуру, а с ним
                # позволяет Pydantic читать данные из атрибутов любого Python-объекта (например, user.name, user.age)

                update_user_dto.can_receive_messages = True
                update_user_dto.telegram_username = user_dto.telegram_username
                await UserRepository.update(update_user_dto, session)
                await session.commit()

    @staticmethod
    def parse_interval(payload: str) -> timedelta:
        mapping = {
            "1 день": timedelta(days=1),
            "7 дней": timedelta(days=7),
            "1 месяц": timedelta(days=30),
            "6 месяцев": timedelta(days=183),
            "1 год": timedelta(days=365)
        }

        return mapping.get(payload, timedelta(days=0))

    @staticmethod
    async def get_my_profile_buttons(telegram_id: int, session: AsyncSession) -> tuple[InputMediaPhoto |
                                                                                       InputMediaVideo |
                                                                                       InputMediaAnimation, InlineKeyboardBuilder]:
        kb_builder = InlineKeyboardBuilder()
        kb_builder.button(text="➕ Пополнить баланс", callback_data=MyProfileCallback.create(level=1))
        kb_builder.button(text="🧾 История покупок", callback_data=MyProfileCallback.create(level=3))
        kb_builder.adjust(2)
        user = await UserRepository.get_by_tgid(telegram_id, session)
        fiat_balance = round(user.top_up_amount - user.consume_records, 2)
        caption = (("👤 <b>Ваш профиль\nID:</b> <code>{telegram_id}</code>\n"
                   "\n<b>Ваш баланс в рублях:</b>")
                   .format(telegram_id=user.telegram_id, fiat_balance=fiat_balance))

        button_media = await ButtonMediaRepository.get_by_button(KeyboardButton.MY_PROFILE, session)
        media = MediaService.convert_to_media(button_media.media_id, caption=caption)
        return media, kb_builder

    @staticmethod
    async def get_top_up_buttons(callback_data: MyProfileCallback) -> tuple[str, InlineKeyboardBuilder]:
        kb_builder = InlineKeyboardBuilder()
        for cryptocurrency in Cryptocurrency:
            kb_builder.button(
                text=cryptocurrency.name,
                callback_data=MyProfileCallback.create(level=callback_data.level + 1,
                                                       cryptocurrency=cryptocurrency)
            )
        kb_builder.adjust(1)
        kb_builder.row(callback_data.get_back_button())
        return "💵 Выберите метод пополнения", kb_builder

    @staticmethod
    async def get_purchase_history_buttons(
                                           callback_data: MyProfileCallback | None,
                                           session: AsyncSession
                                           ) -> tuple[str, InlineKeyboardBuilder]:
        callback_data = callback_data or MyProfileCallback.create(level=3)
        user_id = None
        buys = await BuyRepository.get_by_buyer_id(user_id, callback_data.page, session)
        kb_builder = InlineKeyboardBuilder()
        for buy in buys:
            kb_builder.button(text="📦 Покупка: #{buy_id}  | Итоговая цена: {total_price:.2f} руб.".format(
                buy_id=buy.id,
                total_price=buy.total_price),
                callback_data=MyProfileCallback.create(
                    level=callback_data.level + 1,
                    buy_id=buy.id,
                    user_role=callback_data.user_role
                ))
        kb_builder.adjust(1)

        if len(kb_builder.as_markup().inline_keyboard) > 1 and callback_data.user_role == UserRole.USER:
            caption = "🧾 <b>Ваши покупки:</b>"
        elif len(kb_builder.as_markup().inline_keyboard) > 1 and callback_data.user_role == UserRole.ADMIN:
            caption = "🛍 ️Пожалуйста выберите покупку:"
        else:
            caption = "⚠️ У Вас нет ни одной покупки"
        return caption, kb_builder

