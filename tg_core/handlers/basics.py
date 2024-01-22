from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from tg_core.database.models import async_register, async_session

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
