from sqlalchemy.ext.asyncio import AsyncSession

from models.buy import BuyDTO, Buy


class BuyRepository:

    @staticmethod
    async def create(buy_dto: BuyDTO, session: AsyncSession) -> int:
        buy = Buy(**buy_dto.model_dump())
        session.add(buy)
        await session.flush()
        return buy.id

