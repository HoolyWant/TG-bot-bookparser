import asyncio
import logging
import os
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from tg_core.database.models import async_main
from tg_core.handlers.basics import router

BASE_DIR = Path(__file__).resolve().parent.parent
dot_env = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=dot_env)


async def main():
    await async_main()
    bot = Bot(token=os.getenv('TELEBOT_API_KEY'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

