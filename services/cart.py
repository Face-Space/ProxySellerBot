from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from models.buy import BuyDTO
from models.buyProxy import BuyProxyDTO
from models.cartItem import CartItemDTO
from models.proxies import ProxyDTO
from orm_query.buy import BuyRepository
from orm_query.buyProxy import BuyProxyRepository
from orm_query.cart import CartRepository
from orm_query.cartItem import CartItemRepository
from orm_query.country import CountryRepository
from orm_query.proxies import ProxiesRepository
from orm_query.proxy_type import ProxyTypeRepository
from orm_query.user import UserRepository
from services.notification import NotificationService
from services.proxy_type import ProxyService
from utils.callbacks import ProxyCatalogCallback, CartCallback
from utils.common import add_pagination_buttons, add_pagination_buttons_for_cart


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
        unpacked_cb = None

        if isinstance(message, types.Message):
            page = 0
        else:
            page = CartCallback.unpack(message.data).page
            unpacked_cb = CartCallback.unpack(message.data)
            # меняем в CartItem кол-во определённого прокси
            await CartItemRepository.update_cart_item(unpacked_cb.cart_item_id, user.id, unpacked_cb.cart_qty, session)

        cart_items = await CartItemRepository.get_by_user_id(user.id, 0 , session)
        kb_builder = InlineKeyboardBuilder()

        for cart_item in cart_items:

            if unpacked_cb and unpacked_cb.cart_qty:
                cart_qty = unpacked_cb.cart_qty
            else:
                cart_qty = cart_item.quantity

            proxy_dto = ProxyDTO(country_id=cart_item.country_id, name=cart_item.name,
                                 proxy_type_id=cart_item.proxy_type_id)
            price = await ProxiesRepository.get_price(proxy_dto, session)
            days_count = await ProxyService.calculate_days(cart_item.period_days)

            kb_builder.button(text="\uD83D\uDCE6 {proxy_name} | Сумма: {total_price:.2f} руб.\uD83D\uDDD1 \n".format(
                proxy_name=cart_item.name,
                total_price=cart_qty * price * days_count),
                callback_data=CartCallback.create(1, page, cart_item_id=cart_item.id, cart_qty=cart_qty))

        if len(kb_builder.as_markup().inline_keyboard) > 0:
            cart = await CartRepository.get_or_create(user.id, session)
            unpacked_cb = CartCallback.create(0) if isinstance(message, types.Message) else CartCallback.unpack(message.data)
            kb_builder.button(text="🛍️ Оплатить", callback_data=CartCallback.create(3, page, cart.id))
            kb_builder.adjust(1)
            kb_builder = await add_pagination_buttons(kb_builder, unpacked_cb,
                                                      CartItemRepository.get_maximum_page(user.id, session), None)
            return "🛒 Корзина", kb_builder
        else:
            return "Корзина пуста", kb_builder


    @staticmethod
    async def change_cart_item(callback: CallbackQuery, session: AsyncSession):
        message_text = ""
        unpacked_cb = CartCallback.unpack(callback.data)
        user = await UserRepository.get_by_tgid(callback.from_user.id, session)
        # cart_items = await CartItemRepository.get_all_by_user_id(user.id, session)
        cart_item = await CartItemRepository.get_by_cart_item_id(unpacked_cb.cart_item_id, user.id, session)

        cart_qty = unpacked_cb.cart_qty
        if cart_qty is not None:
            if unpacked_cb.action == "+":
                cart_qty += 1
            elif unpacked_cb.action == "-":
                cart_qty -= 1
            elif unpacked_cb.action == "♾️":
                cart_qty = unpacked_cb.max_qty
        else:
            cart_qty = cart_item.quantity

        proxy_dto = ProxyDTO(country_id=cart_item.country_id, name=cart_item.name,
                             proxy_type_id=cart_item.proxy_type_id)
        price = await ProxiesRepository.get_price(proxy_dto, session)
        proxy_type = await ProxyTypeRepository.get_by_id(cart_item.proxy_type_id, session)
        country = await CountryRepository.get_by_id(cart_item.country_id, session)
        available_qty = await ProxiesRepository.get_available_qty(proxy_dto, session)
        days_count = await ProxyService.calculate_days(cart_item.period_days)

        line_proxy_total = float(price) * float(cart_qty) * days_count
        cart_line_item = ("📦 Название прокси: {proxy_name} \n{country_flag} Страна: {country_name} "
                        "\n💾 Тип прокси: {proxy_type} "
                        "\n💸 Цена: {price:.2f} руб. день/шт."
                        "\n🔢 Количество в корзине: {cart_qty} шт.\n🔢 Доступное количество: {available_qty} "
                        "\n🕐 Период: {period_days} "
                        "\n💰 Итого: {total_price} руб."
                        "\n<i>При нажатии 'Назад к оплате' все изменения автоматически сохраняются!</i>").format(
            proxy_name=cart_item.name,
            country_flag=country.country_flag,
            country_name=country.country_name,
            proxy_type=proxy_type.proxy_type,
            price=price,
            cart_qty=cart_qty,
            available_qty=available_qty,
            period_days=cart_item.period_days,
            total_price=line_proxy_total,
        )
        message_text += cart_line_item

        kb_builder = InlineKeyboardBuilder()
        await add_pagination_buttons_for_cart(kb_builder, unpacked_cb, available_qty, cart_qty, unpacked_cb.cart_item_id)
        kb_builder.row(types.InlineKeyboardButton(text="⬅️ Назад к оплате", callback_data=CartCallback.create(level=0,
                                                  cart_qty=cart_qty, cart_item_id=unpacked_cb.cart_item_id).pack()))

        return message_text, kb_builder


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
                              callback_data=CartCallback.create(2, cart_item_id=cart_item_id, confirmation=True))
            kb_builder.button(text="❌ Отмена", callback_data=CartCallback.create(0))
            return "Удалить товар из корзины?         ", kb_builder


    @staticmethod
    async def __create_checkout_msg(cart_items: list[CartItemDTO], session: AsyncSession) -> tuple[str, int]:
        message_text = "Оформить заказ?"
        message_text += "<b>\n\n"
        cart_grand_total = 0.0

        for cart_item in cart_items:
            proxy_dto = ProxyDTO(country_id=cart_item.country_id, name=cart_item.name, proxy_type_id=cart_item.proxy_type_id)
            price = await ProxiesRepository.get_price(proxy_dto, session)
            proxy_type = await ProxyTypeRepository.get_by_id(cart_item.proxy_type_id, session)
            days_count = await ProxyService.calculate_days(cart_item.period_days)

            line_proxy_total = float(price) * float(cart_item.quantity)
            cart_line_item = ("📦 {proxy_name} \n Тип прокси: {proxy_type} \n Цена: {price:.2f} руб. день/шт.\n"
                              " Количество: {qty} шт.\n Период: {period_days}📑 \n").format(
                proxy_name=cart_item.name, proxy_type=proxy_type.proxy_type, qty=cart_item.quantity,
                price=price, period_days=cart_item.period_days
            )
            cart_grand_total += line_proxy_total * days_count
            message_text += cart_line_item
        message_text += "\n<u>Итого: {cart_grand_total:.2f} руб.</u>".format(
            cart_grand_total=cart_grand_total
        )
        message_text += "</b>"

        return message_text, cart_grand_total


    @staticmethod
    async def checkout_processing(callback: CallbackQuery, session: AsyncSession) -> tuple[str, InlineKeyboardBuilder]:
        user = await UserRepository.get_by_tgid(callback.from_user.id, session)
        cart_items = await CartItemRepository.get_all_by_user_id(user.id, session)
        message_text, cart_grand_total = await CartService.__create_checkout_msg(cart_items, session)
        kb_builder = InlineKeyboardBuilder()
        kb_builder.button(text="✅ Подтвердить", callback_data=CartCallback.create(4, cart_grand_total=cart_grand_total,
                                                                                  confirmation=True))
        kb_builder.button(text="❌ Отмена", callback_data=CartCallback.create(0))
        return message_text, kb_builder


    @staticmethod
    async def buy_processing(callback: CallbackQuery, session: AsyncSession):
        unpacked_cb = CartCallback.unpack(callback.data)
        user = await UserRepository.get_by_tgid(callback.from_user.id, session)
        cart_items = await CartItemRepository.get_all_by_user_id(user.id, session)
        cart_total = 0.0
        out_of_stock = []
        for cart_item in cart_items:
            proxy_dto = ProxyDTO(country_id=cart_item.country_id, name=cart_item.name,
                                 proxy_type_id=cart_item.proxy_type_id)
            price = await ProxiesRepository.get_price(proxy_dto, session)
            cart_total += float(price) * float(cart_item.quantity)
            is_in_stock = await ProxiesRepository.get_available_qty(proxy_dto, session) >= cart_item.quantity
            if is_in_stock is False:
                out_of_stock.append(cart_item)
        is_enough_money = (user.top_up_amount - user.consume_records) >= cart_total
        # user.top_up_amount – сколько всего пользователь пополнил (внес на счёт) за всё время.
        # user.consume_records – сколько уже израсходовано (списаний по покупкам).
        # (user.top_up_amount - user.consume_records) – текущий баланс пользователя (остаток средств).
        # cart_total – общая стоимость всех товаров в корзине.

        kb_builder = InlineKeyboardBuilder()
        if unpacked_cb.confirmation and len(out_of_stock) == 0 and is_enough_money:
            sold_items = []
            msg = "Оплата прошла успешно, спасибо за покупку😉"
            for cart_item in cart_items:
                # price = await ProxiesRepository.get_price(ProxyDTO(country_id=cart_item.country_id,
                #                         name=cart_item.name, proxy_type_id=cart_item.proxy_type_id), session)
                purchased_proxies = await ProxiesRepository.get_purchased_proxies(cart_item.country_id,
                                cart_item.proxy_type_id, cart_item.quantity, cart_item.name, session)
                buy_dto = BuyDTO(buyer_id=user.id, quantity=cart_item.quantity,
                                 total_price=unpacked_cb.cart_grand_total, period_days=cart_item.period_days)
                buy_id = await BuyRepository.create(buy_dto, session)

                # days_count = await ProxyService.calculate_days(cart_item.period_days)
                buy_proxy_dto_list = [BuyProxyDTO(proxy_id=proxy.id, buy_id=buy_id,
                                                  period_days=cart_item.period_days) for proxy in purchased_proxies]
                await BuyProxyRepository.create_many(buy_proxy_dto_list, session)
                for proxy in purchased_proxies:
                    proxy.quantity -= cart_item.quantity
                await ProxiesRepository.update(purchased_proxies, session)
                await CartItemRepository.remove_from_cart(cart_item.id, session)
                sold_items.append(cart_item)
            user.consume_records = user.consume_records + cart_total
            await UserRepository.update(user, session)
            await session.commit()
            await NotificationService.new_buy(sold_items, user, session)
            return msg, kb_builder
        elif unpacked_cb.confirmation is False:
            kb_builder.row(unpacked_cb.get_back_button(0))
            return "❌ Оплата заказа отменена", kb_builder
        elif is_enough_money is False:
            kb_builder.row(unpacked_cb.get_back_button(0))
            return "У вас недостаточно средств для оформления заказа 😔", kb_builder
        elif len(out_of_stock) > 0:
            kb_builder.row(unpacked_cb.get_back_button(0))
            msg = "\u26A0\uFE0F<b>Текущий прокси уже распродан либо его недостаточное количество:</b>\n\n"
            return msg, kb_builder



