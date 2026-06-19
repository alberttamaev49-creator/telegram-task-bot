import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.handlers import router
from app.config import BOT_TOKEN

from app.database import Base, engine
from app.models import Task

logging.basicConfig(level=logging.INFO)


def check_env():
    if not os.getenv("BOT_TOKEN"):
        raise RuntimeError("BOT_TOKEN не задан")

    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL не задан")


check_env()


# ✅ СОЗДАЁМ ТАБЛИЦЫ ПРИ СТАРТЕ
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await create_tables()   # 🔥 ВАЖНО — ДО БОТА

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())