from sqlalchemy.ext.asyncio import AsyncSession

from models.cartItem import CartItemDTO, CartItem


class CartItemRepository:

    @staticmethod
    async def create(cart_item: CartItemDTO, session: AsyncSession):
        cart_item = CartItem(**cart_item.model_dump())
        session.add(cart_item)
        await session.flush()
        return cart_item.id

