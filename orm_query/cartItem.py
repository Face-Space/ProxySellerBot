from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Cart
from models.cartItem import CartItemDTO, CartItem


class CartItemRepository:

    @staticmethod
    async def create(cart_item: CartItemDTO, session: AsyncSession):
        cart_item = CartItem(**cart_item.model_dump())
        session.add(cart_item)
        await session.flush()
        return cart_item.id

    @staticmethod
    async def get_by_user_id(user_id: int, page: int, session: AsyncSession, page_entries = 8) -> list[CartItemDTO]:
        query = select(CartItem).join(Cart, CartItem.cart_id == Cart.id).where(Cart.user_id == user_id).limit(
        page_entries).offset(page_entries * page)
        cart_items = await session.execute(query)
        return [CartItemDTO.model_validate(cart_item, from_attributes=True) for cart_item in
                cart_items.scalars().all()]
