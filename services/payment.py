import re
from datetime import datetime, timezone

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

import qrcode

import config
from FSM.states import UserStates
from crypto_api.CryptoApiWrapper import CryptoApiWrapper
from enums.cryptocurrency import Cryptocurrency
from enums.payment import PaymentType
from models.payment import ProcessingPaymentDTO
from orm_query.payment import PaymentRepository
from orm_query.user import UserRepository
from utils.callbacks import MyProfileCallback


class PaymentService:
    AMOUNT_RE = re.compile(r"^(?:0|[1-9]\d*)(?:\.\d{1,2})?$")

    @staticmethod
    def __create_qr_code(payment_dto: ProcessingPaymentDTO, io=None):
        qr = qrcode.QRCode()
        if payment_dto.cryptoCurrency == Cryptocurrency.BNB:
            qr_data = payment_dto.address
        elif payment_dto.paymentType == PaymentType.PAYMENT:
            qr_data = f"{payment_dto.cryptoCurrency.get_coingecko_name()}:{payment_dto.address}?amount={payment_dto.cryptoAmount}&value={payment_dto.cryptoAmount}"
        else:
            qr_data = f"{payment_dto.cryptoCurrency.get_coingecko_name()}:{payment_dto.address}"
        qr.add_data(qr_data)
        qr.make(fit=True)
        #  Параметр fit=True автоматически подбирает размер сетки под объем данных
        img = qr.make_image()
        buffer = io.BytesIO()
        img.save(buffer)
        buffer.seek(0)
        return BufferedInputFile(
            file=buffer.getvalue(),
            filename=f"{payment_dto.address}.png"
        )

    @staticmethod
    async def __create_invoice(payment_dto: ProcessingPaymentDTO) -> ProcessingPaymentDTO:
        headers = {
            "X-Api-Key": config.KRYPTO_EXPRESS_API_KEY,
            "Content-Type": "application/json"
        }
        payment_dto = await CryptoApiWrapper.fetch_api_request(
            f"{config.KRYPTO_EXPRESS_API_URL}/payment",
            method="POST",
            data=payment_dto.model_dump_json(exclude_none=True), # выкинет из итоговой строки все поля, которые равны None
            headers=headers
        )
        payment_dto = ProcessingPaymentDTO.model_validate(payment_dto, from_attributes=True)
        return payment_dto

    @staticmethod
    def __request_fiat_amount(kb_builder: InlineKeyboardBuilder):
        kb_builder.button(
            text="⬅️ Назад",
            callback_data=MyProfileCallback.create(level=1)
        )
        # bot_photo_id = get_bot_photo_id()
        caption = ("\uD83D\uDCB5 <b>Пожалуйста введите сумму, которую вы хотите пополнить <u>руб.</u>"
                   "\n⚠\uFE0F Внимание! Минимальный депозит 100 руб.</b>")
        media = InputMediaPhoto(media="https://www.google.com/imgres?q=%D0%B4%D0%B5%D0%BD%D1%8C%D0%B3%D"
                                      "0%B8&imgurl=https%3A%2F%2Fhistory.ru%2Fimages%2Farticles%2F32%2F"
                                      "i1TzbLGqmzPr2bxCMZdOUYnVh5OUV2E7F3nADSjF.jpg&imgrefurl=https%3A%2"
                                      "F%2Fhistory.ru%2Fread%2Farticles%2Fkratkaya-istoriya-deneg&docid="
                                      "q_Cyyuea3z8gnM&tbnid=8TJsknxF8ckRLM&vet=12ahUKEwjS35Oyr9eTAxUeEBA"
                                      "IHVNpERYQnPAOegQIGRAB..i&w=1162&h=653&hcb=2&ved=2ahUKEwjS35Oyr9eTA"
                                      "xUeEBAIHVNpERYQnPAOegQIGRAB",
                                caption=caption)

        return media, kb_builder


    @staticmethod
    async def create(callback: CallbackQuery | Message,
                     callback_data: MyProfileCallback | None,
                     state: FSMContext,
                     session: AsyncSession) -> tuple[InputMediaPhoto | str, InlineKeyboardBuilder]:

        user = await UserRepository.get_by_tgid(callback.from_user.id, session)
        unexpired_payments_count = await PaymentRepository.get_unexpired_unpaid_payments(user.id, session)
        state_data = await state.get_data()
        current_state = await state.get_state()
        if callback_data is None:
            cryptocurrency = Cryptocurrency(state_data.get('cryptocurrency'))
        else:
            cryptocurrency = callback_data.cryptocurrency
        kb_builder = InlineKeyboardBuilder()
        if unexpired_payments_count >= 15:
            kb_builder.row(callback_data.get_back_button())
            return "<b>⏳ Слишком много запросов для платежа!\nПожалуйста подождите и попробуйте снова.</b>", kb_builder
        elif cryptocurrency in Cryptocurrency.get_stablecoins() and current_state is None:
            await state.set_state(UserStates.top_up_amount)
            await state.update_data(cryptocurrency=cryptocurrency.value)
            return PaymentService.__request_fiat_amount(kb_builder)
        elif cryptocurrency in Cryptocurrency.get_stablecoins() and current_state == UserStates.top_up_amount:
            message: Message = callback
            fiat_amount = message.html_text
            if PaymentService.AMOUNT_RE.fullmatch(fiat_amount):
                fiat_amount = float(fiat_amount)
                if 100 <= fiat_amount < 1_000_000:
                    await state.set_state()
                    payment_dto = ProcessingPaymentDTO(
                        paymentType=PaymentType.PAYMENT,
                        fiatCurrency="руб.",
                        cryptoCurrency=cryptocurrency,
                        fiatAmount=fiat_amount
                    )
                    message = await message.answer(text= "⏳ Загрузка...")
                    await state.update_data(msg_id=message.message_id, chat_id=message.chat.id)
                    payment_dto = await PaymentService.__create_invoice(payment_dto)
                    await PaymentRepository.create(payment_dto.id, user.id, message.message_id, session)
                    await session.commit()
                    timestamp_s = payment_dto.expireDatetime / 1000
                    dt = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
                    # Берет наши секунды и превращает их в объект «Дата и Время»
                    formatted = dt.strftime('%H:%M UTC on %B %d, %Y')
                    caption = ("\uD83D\uDCB5 <b>Внесите депозит по адресу <code>{crypto_amount}</code> {crypto_name} чтобы"
                            "пополнить баланс на {fiat_amount} руб.</b>\n\nСтатус платежа: {status}"
                            "\nСрок действия платежа до {payment_lifetime}.\n\n<b>Важно</b>\n<i>Для каждого депозита "
                            "присваивается уникальный адрес\nПополнение счета происходит в течение 5 минут после перевода."
                            "\n\nПосле успешного обновления баланса вы получите уведомление от бота.</i>\n"
                            "\n<b>Ваш {crypto_name} адрес\n</b><code>{addr}</code>").format(
                        crypto_name=payment_dto.cryptoCurrency.name,
                        addr=payment_dto.address,
                        crypto_amount=payment_dto.cryptoAmount,
                        fiat_amount=payment_dto.fiatAmount,
                        status="🟡 В ожидании.",
                        payment_lifetime=formatted
                    )
                    qr_code_file = PaymentService.__create_qr_code(payment_dto)
                    return InputMediaPhoto(media=qr_code_file, caption=caption), kb_builder
                else:
                    return PaymentService.__request_fiat_amount(kb_builder)
            else:
                return PaymentService.__request_fiat_amount(kb_builder)
        else:
            message = await callback.message.edit_caption(caption="⏳ Загрузка...")
            payment_dto = ProcessingPaymentDTO(
                paymentType=PaymentType.DEPOSIT,
                fiatCurrency="руб.",
                cryptoCurrency=cryptocurrency
            )
            payment_dto = await PaymentService.__create_invoice(payment_dto)
            await PaymentRepository.create(payment_dto.id, user.id, message.message_id, session)
            await session.commit()
            timestamp_s = payment_dto.expireDatetime / 1000
            dt = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)
            formatted = dt.strftime('%H:%M UTC on %B %d, %Y')
            caption = ("💵 <b>Внесите желаемую сумму на указанный адрес {crypto_name} чтобы пополнить баланс\n"
                       "\nСтатус платежа {status}. Срок действия платежа до {payment_lifetime}</b>\n"
                       "\n<b>Важно</b>\n<i>Указаны уникальные {crypto_name} адреса для каждого депозита.\n"
                       "\nПополнение счета осуществляется в течение 5 минут после перевода. "
                       "После успешного обновления баланса вы получите уведомление от бота</i>\n"
                       "\n<b>Ваш {crypto_name} адрес\n</b><code>{addr}</code>").format(
                crypto_name=payment_dto.cryptoCurrency.name,
                addr=payment_dto.address,
                status="🟡 В ожидании.",
                payment_lifetime=formatted
            )
            qr_code_file = PaymentService.__create_qr_code(payment_dto)
            return InputMediaPhoto(media=qr_code_file, caption=caption), kb_builder


