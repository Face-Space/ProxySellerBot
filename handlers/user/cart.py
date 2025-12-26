from aiogram import Router

cart_router = Router()




@proxy_catalog_router.callback_query(F.data.startswith("quantity"), ProxyCatalog.proxies_quantity)
async def payment_method(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Выберите способ оплаты:", reply_markup=payment_types.as_markup())
    await state.set_state(ProxyCatalog.payment)


@proxy_catalog_router.callback_query(F.data.startswith("payment"), ProxyCatalog.payment)
async def payment(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    payment_type = callback.data.split("_")[1]
    data = await state.get_data()
    price = int(float(data["price"]))
    period_days = data["period_days"]

    if payment_type == "paymaster":

        await bot.send_invoice(
            callback.message.chat.id,
            title=f"Покупка прокси на {period_days} дней",
            description="Покупка прокси",
            provider_token=config.PAYMENT_TOKEN,
            currency="rub",
            prices=[LabeledPrice(label=f"Покупка прокси на {price}", amount=price * 100)],
            start_parameter="subscription",
            payload=f"{period_days}"
        )

    else:
        user_id = callback.from_user.id
        payload = f"user:{user_id}:plan:basic"

        invoice = await cp.create_invoice(
            amount=float(price),
            asset="USDT",
            payload=payload,
        )

        pay_url = invoice["pay_url"]  # или другой URL в ответе API


        await callback.message.answer(
            f"Счёт на {price} USDT. Нажми кнопку для оплаты:",
            reply_markup=confirm_payment(pay_url),
        )

    await state.clear()
