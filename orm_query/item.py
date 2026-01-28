from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Proxies
from models.cartItem import CartItem
from models.item import ItemDTO


class ItemRepository:

    @staticmethod
    async def get_price(item_dto: ItemDTO, session: AsyncSession):
        query = select(CartItem.price).where(CartItem.cart_id)

