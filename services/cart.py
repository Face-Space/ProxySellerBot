from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from orm_query.cart import CartRepository
from orm_query.user import UserRepository
from utils.callbacks import ProxyCatalogCallback


class CartService:

    @staticmethod
    async def add_to_cart(callback: CallbackQuery, session: AsyncSession):
        unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
        user = await UserRepository.get_by_tgid(callback.from_uer.id, session)
        cart = await CartRepository.get_or_create(user.id, session)
        cart_item = CartItemDTO(
            category_id=unpacked_cb.category_id,
            subcategory_id=unpacked_cb.subcategory_id,
            quantity=unpacked_cb.quantity,
            cart_id=cart.id
        )
        await CartRepository.add_to_cart(cart_item, cart, session)
        await session.commit()


