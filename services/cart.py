from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from models.cartItem import CartItemDTO
from models.proxies import ProxyDTO
from orm_query.cart import CartRepository
from orm_query.cartItem import CartItemRepository
from orm_query.proxies import ProxiesRepository
from orm_query.proxy_type import ProxyTypeRepository
from orm_query.user import UserRepository
from utils.callbacks import ProxyCatalogCallback, CartCallback
from utils.common import add_pagination_buttons


class CartService:

    @staticmethod
    async def add_to_cart(callback: CallbackQuery, session: AsyncSession):
        unpacked_cb = ProxyCatalogCallback.unpack(callback.data)
        user = await UserRepository.get_by_tgid(callback.from_user.id, session)
        cart = await CartRepository.get_or_create(user.id, session)

        cart_item = CartItemDTO(
            cart_id=cart.id,
            name=unpacked_cb.proxy_name,
            country_id=unpacked_cb.country_id,
            proxy_type_id=unpacked_cb.proxy_type_id,
            period_days=unpacked_cb.period,
            quantity=unpacked_cb.quantity,
            price=unpacked_cb.price
        )
        await CartRepository.add_to_cart(cart_item, cart, session)
        await session.commit()

    @staticmethod
    async def create_buttons(message: types.Message | CallbackQuery, session: AsyncSession):
        user = await UserRepository.get_by_tgid(message.from_user.id, session)
        page = 0 if isinstance(message, types.Message) else CartCallback.unpack(message.data).page
        cart_items = await CartItemRepository.get_by_user_id(user.id, 0 , session)
        kb_builder = InlineKeyboardBuilder()
        for cart_item in cart_items:
            proxy_dto = ProxyDTO(country_id=cart_item.country_id, name=cart_item.name,
                                 proxy_type_id=cart_item.proxy_type_id)
            price = await ProxiesRepository.get_price(proxy_dto, session)
            proxy_type = await ProxyTypeRepository.get_by_id(cart_item.proxy_type_id, session)
            kb_builder.button(text="\uD83D\uDCE6 {proxy_name}| Цена: {total_price:.2f} руб. \n "
                                   "Количество: {qty} \uD83D\uDDD1 \n".format(
                proxy_name=cart_item.name,
                total_price=cart_item.quantity * price,
                qty=cart_item.quantity),
                callback_data=CartCallback.create(1, page, cart_item_id=cart_item.id))

        if len(kb_builder.as_markup().inline_keyboard) > 0:
            cart = await CartRepository.get_or_create(user.id, session)
            unpacked_cb = CartCallback.create(0) if isinstance(message, types.Message) else CartCallback.unpack(message.data)
            kb_builder.button(text="🛍️ Оплатить", callback_data=CartCallback.create(2, page, cart.id))
            kb_builder.adjust(1)
            kb_builder = await add_pagination_buttons(kb_builder, unpacked_cb,
                                                      CartItemRepository.get_maximum_page(user.id, session), None)
            return "🛒 Корзина", kb_builder
        else:
            return "Корзина пуста", kb_builder

    @staticmethod
    async def delete_cart_item(callback: CallbackQuery, session: AsyncSession):
        unpacked_cb = CartCallback.unpack(callback.data)
        cart_item_id = unpacked_cb.cart_item_id
        kb_builder = InlineKeyboardBuilder()
        if unpacked_cb.confirmation:
            await CartItemRepository.remove_from_cart(cart_item_id, session)
            await session.commit()
            return "Товар удалён из корзины", kb_builder
        else:
            kb_builder.button(text="✅ Подтвердить",
                              callback_data=CartCallback.create(1, cart_item_id=cart_item_id, confirmation=True))
            kb_builder.button(text="❌ Отмена", callback_data=CartCallback.create(0))
            return "Удалить товар из корзины?", kb_builder

    @staticmethod
    async def __create_checkout_msg(cart_items: list[CartItemDTO], session: AsyncSession) -> str:
        message_text = "Оформить заказ?"
        message_text += "<b>\n\n"
        cart_grand_total = 0.0

        for cart_item in cart_items:
            proxy_dto = ProxyDTO(country_id=cart_item.country_id, proxy_type_id=cart_item.proxy_type_id)
            price = await ProxiesRepository.get_price(proxy_dto, session)
            proxy_type = await ProxyTypeRepository.get_by_id(cart_item.proxy_type_id, session)
            line_proxy_total = price * cart_item.quantity

    @staticmethod
    async def checkout_processing(callback: CallbackQuery, session: AsyncSession) -> tuple[str, InlineKeyboardBuilder]:
        user = await UserRepository.get_by_tgid(callback.from_user.id, session)
        cart_items = await CartItemRepository.get_all_by_user_id(user.id, session)
        message_text = await CartService.__create_checkout_msg(cart_items, session)











