from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f

from kbds.reply import get_keyboard

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        'Привет, я виртуальный помощник',
        reply_markup=get_keyboard(
            'История клуба',
            'Состав команды',
            'Титулы',
            'Статистика',
            placeholder='Что вас интересует?',
            sizes=(2, 2)
        ),
    )

@user_private_router.message(or_f(Command('history'), (F.text.lower() == 'история клуба')))
async def menu_cmd(message: types.Message):
    await message.answer('История клуба:')


@user_private_router.message(F.text.lower() == 'состав команды')
@user_private_router.message(Command('players'))
async def about_cmd(message: types.Message):
    await message.answer('Состав вашей любимой команды:')


@user_private_router.message(F.text.lower() == 'титулы')
@user_private_router.message(Command('titles'))
async def payment_cmd(message: types.Message):
    await message.answer('Значимые титула:')


@user_private_router.message((F.text.lower().contains('стат')) | (F.text.lower() == 'статистика'))
@user_private_router.message(Command('statistics'))
async def menu_cmd(message: types.Message):
    await message.answer('Статистики игроков:')
