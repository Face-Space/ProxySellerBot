from sqlalchemy.ext.asyncio import AsyncSession

from models.user import UserDTO
from repositories.user import UserRepository


class UserService:

    @staticmethod
    async def create_if_not_exist(user_dto: UserDTO, session: AsyncSession) -> None:
        user = await UserRepository.get_by_tgid(user_dto.telegram_id, session)
        match user:
            case None:
                user_id = await UserRepository.create(user_dto, session)
                await CartRepository.get_or_create(user_id, session)
                await session_commit(session)
            case _:
                update_user_dto = UserDTO(**user.model_dump())
                update_user_dto.can_receive_messages = True
                update_user_dto.telegram_username = user_dto.telegram_username
                await UserRepository.update(update_user_dto, session)
                await session_commit(session)