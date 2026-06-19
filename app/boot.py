import asyncio
import logging

from aiogram import Bot, Dispatcher
from app.config import BOT_TOKEN
from app.handlers import router

logging.basicConfig(level=logging.INFO)


async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is empty!")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())