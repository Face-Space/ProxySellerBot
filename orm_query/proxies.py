from aiogram.types import CallbackQuery
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models import Proxies
from models.proxies import ProxyDTO
from utils.callbacks import ProxyCatalogCallback


class ProxiesRepository:

    @staticmethod
    async def get_available_proxies(country_id: int, proxy_type_id: int, session: AsyncSession):
        query = (select(Proxies)
                 .where(Proxies.country_id == country_id,
                        Proxies.proxy_type_id == proxy_type_id,
                        Proxies.quantity != 0))
        proxies_result = await session.execute(query)
        proxies = proxies_result.scalars().all()
        return [ProxyDTO.model_validate(proxy, from_attributes=True) for proxy in proxies]


    @staticmethod
    async def get_single(country_id: int, proxy_type_id: int, proxy_name: str, session: AsyncSession):
        query = (select(Proxies)
                 .where(Proxies.country_id == country_id,
                        Proxies.proxy_type_id == proxy_type_id,
                        Proxies.name == proxy_name,
                        Proxies.quantity != 0))
        proxy = await session.execute(query)
        return ProxyDTO.model_validate(proxy.scalar(), from_attributes=True)


    @staticmethod
    async def get_available_qty(proxy_dto: ProxyDTO, session: AsyncSession) -> int:
        query = (select(Proxies.quantity)
                 .where(Proxies.country_id == proxy_dto.country_id,
                        Proxies.proxy_type_id == proxy_dto.proxy_type_id,
                        Proxies.name == proxy_dto.name,
                        Proxies.quantity !=0))
        available_qty = await session.execute(query)
        return available_qty.scalar()


    @staticmethod
    async def get_price(proxy_dto: ProxyDTO, session: AsyncSession) -> float:
        query = (select(Proxies.price)
                 .where(Proxies.country_id == proxy_dto.country_id,
                        Proxies.name == proxy_dto.name,
                        Proxies.proxy_type_id == proxy_dto.proxy_type_id))
        price = await session.execute(query)
        return price.scalar()


    @staticmethod
    async def get_purchased_proxies(country_id: int, proxy_type_id: int, quantity: int, name: str, session: AsyncSession) -> list[ProxyDTO]:
        query = (select(Proxies)
        .where(Proxies.country_id == country_id,
               Proxies.proxy_type_id == proxy_type_id,
               Proxies.name == name,
               Proxies.quantity != 0).limit(quantity))
        proxies = await session.execute(query)
        return [ProxyDTO.model_validate(proxy, from_attributes=True) for proxy in proxies.scalars().all()]



