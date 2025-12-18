import uvicorn
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Update, BufferedInputFile
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import traceback

from redis.asyncio import Redis

import config
from bot_setup import bot
from config import *
from database.engine import create_db, session_maker
from handlers.user.user_private import user_router
from middlewares.db import DataBaseSession
from services.notification import NotificationService

redis = Redis(host=config.REDIS_HOST, password=config.REDIS_PASSWORD)
# redis = Redis.from_url("redis://localhost:6379/0")
dp = Dispatcher(storage=RedisStorage(redis=redis))
logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(my_app: FastAPI):
    # защита от повторного импорта роутеров ювикорном
    if not hasattr(user_router, '_parent_router') or user_router._parent_router is None:
        dp.include_router(user_router)


    # === startup ===
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)

    await create_db()
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    for admin in ADMIN_ID_LIST:
        try:
            await bot.send_message(admin, "Бот успешно запущен")
        except Exception as e:
            logger.warning(e)
    yield

    # === shutdown ===
    logger.warning("Shutting down...")
    await bot.delete_webhook()
    await bot.session.close()

    await dp.storage.close()  # Закрывает пул Aiogram
    await redis.aclose()  # Закрывает базовое соединение

    for admin in ADMIN_ID_LIST:
        try:
            await bot.send_message(admin, "Бот лёг")
        except Exception as e:
            logger.warning(e)


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
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
    # try:
    # setup_logging()

    uvicorn.run("bot:app", reload=True)

    # except Exception as e:
    #     print(e)
    #     logger.error(f"Ошибка запуска бота: {e}")

    # Убери GlobalData в D:\MyPetProjects\ProxySellerBot\keyboards\inline.py !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


if __name__ == "__main__":
    main()


