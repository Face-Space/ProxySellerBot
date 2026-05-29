from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import config
from models.base import Base
import os
import shutil


engine = create_async_engine(config.DB_URL, echo=False)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=True)


async def create_db():
    # sql_file_path = "all_my_data.sql"
    #
    # if os.path.exists(sql_file_path):
    #     print("🚀 Обнаружен файл с данными all_my_data.sql. Начинаю потоковый импорт...")
    #
    #     # Используем connect() вместо begin(), чтобы иметь контроль над отдельными транзакциями
    #     async with engine.connect() as conn:
    #         with open(sql_file_path, "r", encoding="utf-8", errors="ignore") as f:
    #             for line in f:
    #                 clean_line = line.strip()
    #
    #                 if not clean_line or clean_line.startswith("--") or clean_line.startswith("SET "):
    #                     continue
    #
    #                 if not clean_line.upper().startswith("INSERT "):
    #                     continue
    #
    #                 # Для каждой отдельной строки создаем свою изолированную транзакцию
    #                 async with conn.begin():
    #                     try:
    #                         await conn.execute(text(clean_line))
    #                     except Exception as e:
    #                         err_str = str(e).lower()
    #                         # Просто пропускаем дубликаты или системный мусор Django
    #                         if "already exists" in err_str or "duplicate key" in err_str or "does not exist" in err_str:
    #                             continue
    #                         print(f"⚠️ Строка пропущена: {clean_line[:60]}... Ошибка: {e}")
    #
    #     print("✅ Все живые данные успешно перенесены в базу Amvera!")
    #
    #     # Исправляем Cross-device link: используем shutil.move вместо os.rename
    #     try:
    #         shutil.move(sql_file_path, "/data/all_my_data.sql.imported")
    #         print("📁 Файл данных безопасно перемещен в постоянное хранилище /data")
    #     except Exception as e:
    #         print(f"⚠️ Не удалось переместить файл в /data: {e}")
    # else:
    #     print("ℹ️ Файл данных не найден. Импорт не требуется.")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

