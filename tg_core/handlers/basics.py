import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from tg_core.database.models import async_register, async_session
from tg_core.handlers.services import parser, clear_list

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Допро пожаловать в парсер-бот! Для регистрации и дальнейшей работы,'
                         'зарегистрируйтесь с помощью команды /register')


@router.message(Command('register'))
async def cmd_register(message: Message):
    fullname = message.from_user.full_name
    await async_register(async_session, fullname)
    await message.answer(
        f"Hello, {message.from_user.full_name}! Вы зарегистрированы!\n "
        f"Введите ссылку на категорию\n"
    )


@router.message(F.text)
async def cmd_link(message: Message):
    await message.answer(
        f"Ожидайте..."
    )
    loop = asyncio.get_event_loop()
    data1 = loop.run_until_complete(parser(message.text))
    data2 = loop.run_until_complete(parser(data1))
    data3 = clear_list(data1, data2)
