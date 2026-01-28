from sqlalchemy import select, join, distinct
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


