from aiogram import types
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from models.cartItem import CartItemDTO
from orm_query.cart import CartRepository
from orm_query.cartItem import CartItemRepository
from orm_query.user import UserRepository
from utils.callbacks import ProxyCatalogCallback, CartCallback


class CartService:

    @staticmethod
    async def add_to_cart(callback: CallbackQuery, session: AsyncSession):
        unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
        user = await UserRepository.get_by_tgid(callback.from_user.id, session)
        cart = await CartRepository.get_or_create(user.id, session)


        cart_item = CartItemDTO(
            # id=unpacked_cb.id,
            quantity=unpacked_cb.quantity,
            cart_id=cart.id
        )
        await CartRepository.add_to_cart(cart_item, cart, session)
        await session.commit()

    @staticmethod
    async def create_buttons(message: types.Message | CallbackQuery, session: AsyncSession):
        user = await UserRepository.get_by_tgid(message.from_user.id, session)
        page = 0 if isinstance(message, types.Message) else CartCallback.unpack(message.data).page
        cart_items = await CartItemRepository.get_by_user_id(user.id, 0 , session)















