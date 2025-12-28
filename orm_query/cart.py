from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.cart import Cart, CartDTO
from models.cartItem import CartItemDTO, CartItem


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

    @staticmethod
    async def add_to_cart(cart_item: CartItemDTO, cart: CartDTO, session: AsyncSession):
        get_old_cart_content = select(Cart).join(
            CartItem, Cart.id == CartItem.cart_id).where(
            Cart.id == cart.id)




