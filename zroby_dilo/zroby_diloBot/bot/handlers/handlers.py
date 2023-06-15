import logging

from aiogram import F
from aiogram import types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext


from aiogram_forms import FormsManager

from .dispatcher import dp, router, bot
from ..models import *
from ..forms import *
from ..views import *
from .filters import *
from ..infrastructure.enums import *

import asyncio



@dp.message(Command(commands=['start']))
async def start_command(message: types.Message):
    intro = "Зроби-діло бот призначений для нагадування, вкажи свою ціль і прямуй до неї. Кличте /help для інструктажу"
    kb = [[types.KeyboardButton(text='/add_aim')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    await message.answer(intro, reply_markup=keyboard)



@dp.message(Command(commands=['help']))
async def help_command(message: types.Message):
    HELPFUL_REPLY = f"/start– знайомство із ботом" \
                    f"\n/help–допомога" \
                    f"\n/add_aim, add– щоб додати нагадування до цілі, назву вводьте в імперативі" \
                    f"\n/cancel_add, cancel– якщо передумали додати ціль" \
                    f"\n/todo_list, /todo, /td– команда виклику списку справ і цілей," \
                    f" щоб отримати незроблені, допишіть todo," \
                    f" для завершених допишіть done," \
                    f" аби побачити всі– пишіть all," \
                    f" за замовчуванням мод– це todo"

    await message.answer(HELPFUL_REPLY)


@dp.message(Command(commands=['add_aim', 'add']))
async def add_aim_command(message: types.Message, forms: FormsManager):
    await forms.show('aimform')


@dp.message(Command(commands=['cancel_add', 'cancel']))
async def cancel_add_command(message: types.Message, state: FSMContext):
    if state.get_state():
        state.clear()
        await message.answer('передумали🙃')

    else:
        return




@dp.message(Command(commands=['todo', 'todo_list', 'td']), AftercommandFullCheck(allow_no_argument=True, modes=TodoListModes))
async def todo_list_command(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    properties = {'user_id': user_id}
    if command.args:
        mode = command.args
        properties['mode'] = mode

    user_todo_list = await todo_list(**properties)
    await message.answer(user_todo_list)

