from aiogram import Router, F, types
from sqlalchemy.ext.asyncio import AsyncSession

proxy_categories_router = Router()



@proxy_categories_router.message(F.text == "Каталог прокси")
async def proxy_categories_text_message(message: types.message, session: AsyncSession):
    await proxy_categories(callback=message, session=session)


async def proxy_categories(**kwargs):
    message = kwargs.get("callback")
    session = kwargs.get("session")
    if isinstance

