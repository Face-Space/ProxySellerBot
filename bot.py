from pathlib import Path
import uvicorn
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Update, BufferedInputFile
# from alembic import command
# from alembic.config import Config
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
import logging
import traceback
import django
from redis.asyncio import Redis


import config
from config import *
from database.engine import create_db, session_maker

from handlers.user.cart import cart_router
from handlers.user.contact_admin import contact_router
from handlers.user.my_profile import my_profile_router
from handlers.user.proxy_catalog import proxy_catalog_router
from handlers.user.user_private import user_router
from middlewares.db import DataBaseSession
from services.notification import NotificationService
from handlers.admin.commands import admin_router


redis = Redis(host=REDIS_HOST, password=REDIS_PASSWORD)
load_dotenv(find_dotenv())
bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=RedisStorage(redis=redis))
logger = logging.getLogger(__name__)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


# Чтобы объект можно было засунуть в конструкцию async with, у него должны быть специальные скрытые методы __aenter__
# (что делать на входе) и __aexit__ (что делать на выходе).Написание этих методов вручную требует много шаблонного кода.
# Декоратор @asynccontextmanager — это магия-помощник, которая берет вашу функцию с одним yield и автоматически
# превращает её в полноценный объект, понятный для async with.
@asynccontextmanager
async def lifespan(my_app: FastAPI):
    await create_db()

    # === startup ===
    dp.include_routers(admin_router, proxy_catalog_router, cart_router, my_profile_router, contact_router,
                       user_router)
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL, secret_token=WEBHOOK_SECRET_TOKEN ,drop_pending_updates=True)

    static = Path("static")
    if not static.exists():
        static.mkdir(parents=True, exist_ok=True)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    for admin in ADMIN_ID_LIST:
        try:
            await bot.send_message(admin, "Бот успешно запущен")
        except Exception as e:
            logger.warning(e)
    yield

    # === shutdown ===
    for admin in ADMIN_ID_LIST:
        try:
            await bot.send_message(admin, "Бот лёг")
        except Exception as e:
            logger.warning(e)
    logger.warning("Shutting down...")
    await bot.delete_webhook()
    await bot.session.close()
    await dp.storage.close()  # Закрывает пул Aiogram
    await redis.aclose()  # Закрывает базовое соединение


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    # Защита вебхука: проверяем секретный токен, присланный Telegram
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret_token != WEBHOOK_SECRET_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    try:
        update_data = await request.json()
        # Метод request.json() асинхронно считывает тело HTTP-запроса и преобразует его
        # из формата JSON в объект Python, обычно это словарь.
        update = Update(**update_data)
        logger.info(f"Received update: {update}")
        await dp.feed_webhook_update(bot, update)
        # Передаёт полученные данные диспетчеру dp с методом feed_webhook_update.
        # Обрабатывает обновление и управляет внутренней логикой aiogram для webhook.

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return {"status": "error"}, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.post("/crypto/callback")
async def crypto_callback(request: Request):
    data = await request.json()

    # 1. Проверить подпись/секрет (документация сервиса)
    # 2. Проверить статус: paid/finished
    # 3. Извлечь payload и найти заказ
    payload = data["payload"]  # "user:123:plan:basic"
    status = data["status"]    # зависит от сервиса

    if status != "paid":
        return {"ok": True}

    # обновить заказ в БД, выдать доступ и т.п.
    # ...

    return {"ok": True}

@app.exception_handler(Exception)
async def exception_handler(exc: Exception):
    traceback_str = traceback.format_exc()
    admin_notification = (
        f"Critical error caused by {exc}\n\n"
        f"Stack trace:\n{traceback_str}"
    )
    if len(admin_notification) > 4096:
        byte_array = bytearray(admin_notification, "utf-8")
        admin_notification = BufferedInputFile(byte_array, "exception.txt")
        # BufferedInputFile(byte_array, "exception.txt") создаёт файл в памяти с именем "exception.txt",
        # который бот может отправить как документ вместо текста
    await NotificationService.send_to_admins(admin_notification, None)
    return JSONResponse(
        status_code=500,
        content={"message": f"An error occured: {str(exc)}"}
    )

def main():
    try:
        # setup_logging()
        db_url = os.getenv('DB_URL')
        uvicorn.run("bot:app", host="0.0.0.0", port=80, proxy_headers=True, forwarded_allow_ips="*")
        # С этой строкой proxy_headers=True: Uvicorn начинает читать специальные технические заголовки (X-Forwarded-For и X-Forwarded-Proto),
        # которые Amvera автоматически прикрепляет к каждому запросу от Telegram. Через них бот узнает настоящий
        # IP-адрес отправителя и понимает, что изначально запрос пришел по HTTPS

        # По умолчанию в целях безопасности Uvicorn соглашается читать прокси-заголовки только в том случае,
        # если они пришли строго с локального адреса 127.0.0.1 [1].Но в облачных архитектурах (таких как Amvera
        # или Docker) внутренний IP-адрес прокси-сервера хостинга постоянно меняется при каждом перезапуске [1].
        # Значение "*" дает команду вашему Uvicorn: «Доверяй заголовкам X-Forwarded-... с абсолютно любого внутреннего
        # IP-адреса»
    except Exception as e:
        print(e)
        logger.error(f"Ошибка запуска бота: {e}")


# dp.include_routers(admin_router, proxy_catalog_router, cart_router, my_profile_router, contact_router, user_router)
#
#
# async def _on_startup():
#     await create_db()
#     for admin in ADMIN_ID_LIST:
#         try:
#             await bot.send_message(admin, "Бот работает для всех")
#         except Exception as e:
#             print(f"Не удалось отправить сообщение админу {admin}: {e}")
#     print("Бот работает для всех")
#
#
# async def _on_shutdown():
#     for admin in ADMIN_ID_LIST:
#         await bot.send_message(admin, "Бот лёг")
#     print("Бот лёг")

# async def init_db():
#     alembic_cfg = Config("alembic.ini")
#     command.upgrade(alembic_cfg, "head")  # Всегда актуальная БД


# async def main():
#     try:
#         logger.info("Запуск телеграм бота")
#         # setup_logging()
#         dp.startup.register(_on_startup)
#         dp.shutdown.register(_on_shutdown)
#         dp.update.middleware(DataBaseSession(session_pool=session_maker))
#
#         # await init_db()
#         await bot.delete_webhook(drop_pending_updates=True)
#         await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
#
#     except Exception as e:
#         print(f"Ошибка запуска бота: {e}")
#         traceback.print_exc()
#
# if __name__ == "__main__":
#     asyncio.run(main())


if __name__ == "__main__":
    main()


# python -c "import secrets; print(secrets.token_urlsafe(32))" - генерация паролей



