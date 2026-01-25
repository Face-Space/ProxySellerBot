from aiogram.types import CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Proxies
from utils.callbacks import ProxyCatalogCallback


class ProxiesRepository:

    @staticmethod
    async def get_proxy(callback: CallbackQuery, session: AsyncSession):
        unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
        country = unpacked_cb.country
        proxy_type = unpacked_cb.proxy_type

        query = select(Proxies).where(
            Proxies.country == country,
            Proxies.proxy_type == proxy_type,
        )
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_quantity(session: AsyncSession, proxy_name: str):
        query = select(Proxies).where(Proxies.name == proxy_name)
        result = await session.execute(query)
        return result.scalar_one_or_none()

