import math

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

import config
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
    async def get_by_user_id(user_id: int, page: int, session: AsyncSession) -> list[CartItemDTO]:
        query = select(CartItem).join(Cart, CartItem.cart_id == Cart.id).where(Cart.user_id == user_id).limit(
        config.PAGE_ENTRIES).offset(config.PAGE_ENTRIES * page)
        cart_items = await session.execute(query)
        return [CartItemDTO.model_validate(cart_item, from_attributes=True) for cart_item in
                cart_items.scalars().all()]

    @staticmethod
    async def get_maximum_page(user_id: int, session: AsyncSession) -> int:
        max_page = len(await CartItemRepository.get_all_by_user_id(user_id, session))
        if max_page % config.PAGE_ENTRIES == 0:
            return max_page / config.PAGE_ENTRIES - 1
        else:
            return math.trunc(max_page / config.PAGE_ENTRIES)

    @staticmethod
    async def get_all_by_user_id(user_id: int, session:AsyncSession) -> list[CartItemDTO]:
        query = select(CartItem).join(Cart, CartItem.cart_id == Cart.id).where(Cart.user_id == user_id)
        cart_items = await session.execute(query)
        return [CartItemDTO.model_validate(cart_item, from_attributes=True) for cart_item in cart_items.scalars().all()]

    @staticmethod
    async def remove_from_cart(cart_item_id: int, session: AsyncSession):
        query = delete(CartItem).where(CartItem.id == cart_item_id)
        await session.execute(query)



