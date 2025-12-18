from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


from models.user import UserDTO, User


class UserRepository:
    @staticmethod
    async def get_by_tgid(telegram_id: int, session: AsyncSession) -> UserDTO | None:
        query = select(User).where(User.telegram_id == telegram_id)
        user = await session.execute(query)
        user = user.scalar()
        if user is not None:
            return UserDTO.model_validate(user, from_attributes=True)
            # model_validate() создаёт экземпляр модели из произвольных данных (словарь, JSON, объект),
            # проверяя их на соответствие схеме. Он автоматически преобразует типы, валидирует значения
            # и выбрасывает ValidationError, если данные некорректны.
            # Параметр from_attributes=True указывает Pydantic извлекать значения из атрибутов объекта user,
            # а не из словаря, что идеально для конвертации моделей БД в DTO
        else:
            return user


    @staticmethod
    async def create(user_dto: UserDTO, session: AsyncSession) -> int:
        user = User(**user_dto.model_dump())
        # model_dump() может конвертировать и DTO и ORM в питон-словарь!
        session.add(user)
        await session.flush()
        return user.id


    @staticmethod
    async def update(user_dto: UserDTO, session: AsyncSession) -> None:
        user_dto_dict = user_dto.model_dump()
        none_keys = [k for k, v in user_dto_dict.items() if v is None]
        for k in none_keys:
            user_dto_dict.pop(k)
        query = update(User).where(User.telegram_id == user_dto.telegram_id).values(**user_dto_dict)
        await session.execute(query)
