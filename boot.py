import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.handlers import router
from app.config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logging.getLogger("aiogram").setLevel(logging.INFO)


def check_env():
    missing = []

    if not os.getenv("BOT_TOKEN"):
        missing.append("BOT_TOKEN")

    if not os.getenv("DATABASE_URL"):
        missing.append("DATABASE_URL")

    if missing:
        raise RuntimeError(f"Не заданы переменные: {', '.join(missing)}")


check_env()


async def main():
    bot = Bot(token=BOT_TOKEN)

    # FIX HERE
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())