from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Proxies


async def get_proxy(session: AsyncSession, data: dict):
    query = select(Proxies).where(Proxies.country == data["country_name"])
    result = await session.execute(query)
    return result.scalars().all()

