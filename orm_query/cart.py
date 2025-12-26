from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.cart import Cart, CartDTO


class CartRepository:

    @staticmethod
    async def get_or_create(user_id: int, session: AsyncSession):
        query = select(Cart).where(Cart.user_id == user_id)
        cart = await session.execute(query)
        cart = cart.scalar()
        if cart is None:
            cart = Cart(user_id=user_id)
            session.add(cart)
            await session.flush()
            return CartDTO.model_validate(cart, from_attributes=True)

        else:
            return CartDTO.model_validate(cart, from_attributes=True)