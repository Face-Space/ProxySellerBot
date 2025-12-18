from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Proxies


class ProxiesRepository:

    @staticmethod
    async def get_proxy(session: AsyncSession, data: dict):
        query = select(Proxies).where(
            Proxies.country == data["country_name"],
                        Proxies.proxy_type == data["proxy_type"],
                        Proxies.period_days == data["period_days"]
        )
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_quantity(session: AsyncSession, proxy_name: str):
        query = select(Proxies).where(Proxies.name == proxy_name)
        result = await session.execute(query)
        return result.scalar_one_or_none()

