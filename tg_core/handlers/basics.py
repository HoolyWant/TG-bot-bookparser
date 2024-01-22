import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

from tg_core.database.models import async_register, async_session
from tg_core.handlers.services import parser, clear_list, cvs_writer, parser_view
import nest_asyncio

nest_asyncio.apply()
router = Router()
file = FSInputFile('parser.csv')


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
    data2 = loop.run_until_complete(parser_view(data1))
    data3 = await clear_list(data1, data2)
    await cvs_writer(data3)
    await message.answer(
        f"Пожалуйста, книги в категории {data3[0]['category']}:"
    )
    await message.answer_document(file)
