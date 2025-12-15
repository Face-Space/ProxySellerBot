from sqlalchemy import select
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
            # Параметр from_attributes=True указывает Pydantic извлекать значения из атрибутов объекта user,
            # а не из словаря, что идеально для конвертации моделей БД в DTO
        else:
            return user

    @staticmethod
    async def create(user_dto: UserDTO, session: AsyncSession) -> int:
        user = User(**user_dto.model_dump())
        session.add(user)
        await session.flush()
        return user.id
