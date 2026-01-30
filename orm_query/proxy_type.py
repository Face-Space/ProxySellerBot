import math

from sqlalchemy import select, join, distinct, func
from sqlalchemy.ext.asyncio import AsyncSession

import config
from models import Proxies
from models.proxy_type import ProxyTypeDTO, ProxyType


class ProxyTypeRepository:

    @staticmethod
    async def get_paginated_by_country_id(country_id: int, page: int, session: AsyncSession) -> list[ProxyTypeDTO]:
        query = (select(ProxyType)
                .join(Proxies, Proxies.proxy_type_id == ProxyType.id)
                .where(Proxies.country_id == country_id, Proxies.quantity != 0)
                .distinct()
                .limit(config.PAGE_ENTRIES)
                .offset(page * config.PAGE_ENTRIES))

        proxy_types = await session.execute(query)
        proxy_types = proxy_types.scalars().all()
        return [ProxyTypeDTO.model_validate(proxy_type, from_attributes=True) for proxy_type in proxy_types]


    @staticmethod
    async def max_page(country_id: int, session: AsyncSession) -> int:
        sub_query = (select(ProxyType.id)
                    .join(Proxies, Proxies.proxy_type_id == ProxyType.id)
                    .where(Proxies.country_id == country_id, Proxies.quantity != 0)
                    .distinct().subquery())
        query = select(func.count()).select_from(sub_query)
        maximum_page = await session.execute(query)
        maximum_page = maximum_page.scalar_one()
        if maximum_page % config.PAGE_ENTRIES == 0:
            return maximum_page / config.PAGE_ENTRIES - 1
        else:
            return math.trunc(maximum_page / config.PAGE_ENTRIES)

    @staticmethod
    async def get_by_id(proxy_type_id: int, session: AsyncSession) -> ProxyTypeDTO:
        query = select(ProxyType).where(ProxyType.id == proxy_type_id)
        proxy_type = await session.execute(query)
        return ProxyTypeDTO.model_validate(proxy_type.scalar(), from_attributes=True)




