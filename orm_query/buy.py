from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import config
from models.buy import BuyDTO, Buy


class BuyRepository:

    @staticmethod
    async def create(buy_dto: BuyDTO, session: AsyncSession) -> int:
        buy = Buy(**buy_dto.model_dump())
        session.add(buy)
        await session.flush()
        return buy.id

    @staticmethod
    async def get_by_buyer_id(
                              user_id: int | None,
                              page: int,
                              session: AsyncSession) -> list[BuyDTO]:
        conditions = []
        if user_id:
            conditions.append(Buy.buyer_id == user_id)
        query = select(Buy).where(*conditions).limit(config.PAGE_ENTRIES).offset(page * config.PAGE_ENTRIES)
        buys = await session.execute(query)
        return [BuyDTO.model_validate(buy, from_attributes=True) for buy in buys.scalars().all()]



