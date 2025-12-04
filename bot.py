import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, Request, status
from contextlib import asynccontextmanager
import logging

from config import *
from handlers.user_private import user_router

bot = Bot(token=TOKEN)
dp = Dispatcher()
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
    await bot.send_message(5138537564, "Бот успешно запущен")
    yield

    # === shutdown ===
    logger.warning("Shutting down...")
    await bot.delete_webhook()
    await bot.session.close()
    await bot.send_message(5138537564, "Бот лёг")


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



def main():
    # try:
    # setup_logging()

    print(f"Зарегистрированные обработчики в user_router: {user_router.resolve_used_update_types()}")
    uvicorn.run("bot:app", reload=True)

    # except Exception as e:
    #     print(e)
    #     logger.error(f"Ошибка запуска бота: {e}")


if __name__ == "__main__":
    main()


