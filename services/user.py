from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from models.user import UserDTO
from orm_query.user import UserRepository
from orm_query.cart import CartRepository


class UserService:

    @staticmethod
    async def create_if_not_exist(user_dto: UserDTO, session: AsyncSession) -> None:
        user = await UserRepository.get_by_tgid(user_dto.telegram_id, session)
        match user:
            case None:
                user_id = await UserRepository.create(user_dto, session)
                await CartRepository.get_or_create(user_id, session)
                # мы почему-то создаём корзину для юзера тогда, когда пользователь нажал на /start
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