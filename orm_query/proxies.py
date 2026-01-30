from aiogram.types import CallbackQuery
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import Proxies
from models.proxies import ProxyDTO
from utils.callbacks import ProxyCatalogCallback


class ProxiesRepository:

    @staticmethod
    async def get_single(country_id: int, proxy_type_id: int, session: AsyncSession):
        query = (select(Proxies)
                 .where(Proxies.country_id == country_id,
                        Proxies.proxy_type_id == proxy_type_id,
                        Proxies.quantity != 0)
                 .limit(1))
        proxy = await session.execute(query)
        return ProxyDTO.model_validate(proxy.scalar(), from_attributes=True)


    @staticmethod
    async def get_available_qty(proxy_dto: ProxyDTO, session: AsyncSession) -> int:
        sub_query = (select(Proxies)
                     .where(Proxies.country_id == proxy_dto.country_id,
                            Proxies.proxy_type_id == proxy_dto.proxy_type_id,
                            Proxies.quantity != 0).subquery())
        query = select(func.count()).select_from(sub_query)
        available_qty = await session.execute(query)
        return available_qty.scalar()



    # @staticmethod
    # async def get_proxy(callback: CallbackQuery, session: AsyncSession):
    #     unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
    #     country = unpacked_cb.country
    #     proxy_type = unpacked_cb.proxy_type
    #
    #     query = select(Proxies).where(
    #         Proxies.country == country,
    #         Proxies.proxy_type == proxy_type,
    #     )
    #     result = await session.execute(query)
    #     return result.scalars().all()
    #
    # @staticmethod
    # async def get_quantity(session: AsyncSession, proxy_name: str):
    #     query = select(Proxies).where(Proxies.name == proxy_name)
    #     result = await session.execute(query)
    #     return result.scalar_one_or_none()

