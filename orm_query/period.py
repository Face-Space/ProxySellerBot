from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.periods import Period, PeriodDTO


class PeriodRepository:

    @staticmethod
    async def get_all_periods(session: AsyncSession):
        query = select(Period)
        periods = await session.execute(query)
        period_names = periods.scalars().all()
        return [PeriodDTO.model_validate(period, from_attributes=True) for period in period_names]