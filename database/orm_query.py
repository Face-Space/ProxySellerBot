from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Proxies


async def get_proxy_country(session: AsyncSession, country_name: str):
    query = select(Proxies).where(Proxies.country == country_name)
    result = await session.execute(query)
    return result.scalars().all()

