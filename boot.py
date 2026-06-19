import asyncio
import logging
import os

logging.basicConfig(level=logging.INFO)


def check_env():
    missing = []

    if not os.getenv("BOT_TOKEN"):
        missing.append("BOT_TOKEN")

    if not os.getenv("DATABASE_URL"):
        missing.append("DATABASE_URL")

    if missing:
        raise RuntimeError(f"Не заданы переменные: {', '.join(missing)}")


check_env()  # ← ВАЖНО: ДО ВСЕХ ИМПОРТОВ БД

from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database import init_db
from app.config import BOT_TOKEN


async def main():
    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())