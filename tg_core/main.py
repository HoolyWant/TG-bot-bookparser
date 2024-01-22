import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from tg_core.database.models import async_main, async_register
from tg_core.handlers.basics import router

dot_env = '.env'
load_dotenv(dotenv_path=dot_env)


async def main():
    await async_main()
    bot = Bot(token='6714894351:AAETPq9TzSUCC8ApEUhIrzg9Ps1i-ROIvYg')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

