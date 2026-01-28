import math

from sqlalchemy import select, join, func
from sqlalchemy.ext.asyncio import AsyncSession

import config
from models import Proxies
from models.country import CountryDTO, Country


class CountryRepository:

    @staticmethod
    async def get(page: int, session: AsyncSession) -> list[CountryDTO]:
        query = (select(Country)
            .join(Proxies, Proxies.country_id == Country.id)
            .where(Proxies.quantity != 0)
            .distinct()
            .limit(config.PAGE_ENTRIES)
            .offset(page * config.PAGE_ENTRIES))

        country_names = await session.execute(query)
        countries = country_names.scalars().all()
        return [CountryDTO.model_validate(country, from_attributes=True) for country in countries]

    @staticmethod
    async def get_maximum_page(session: AsyncSession) -> int:
        unique_country_subquery = (
            select(Country.id)
            .join(Proxies, Proxies.country_id == Country.id)
            .where(Proxies.quantity == 0)
            .distinct()
        ).alias("unique_countries")
        query = select(func.count()).select_from(unique_country_subquery)
        max_page = await session.execute(query)
        max_page = max_page.scalar_one()
        if max_page % config.PAGE_ENTRIES == 0:
            return max_page / config.PAGE_ENTRIES - 1
        else:
            return math.trunc(max_page / config.PAGE_ENTRIES)









