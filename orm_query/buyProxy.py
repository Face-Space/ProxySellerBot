from sqlalchemy.ext.asyncio import AsyncSession

from models.buyProxy import BuyProxyDTO, BuyProxy


class BuyProxyRepository:

    @staticmethod
    async def create_many(buy_proxy_dto_list: list[BuyProxyDTO], session: AsyncSession):
        for buy_proxy_dto in buy_proxy_dto_list:
            session.add(BuyProxy(**buy_proxy_dto.model_dump()))
