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
    intro = "Зроби діло бот призначений для нагадування,вкажи свою ціль і прямуй до неї. " \


    await message.answer(intro)


@dp.message(Command(commands=['help']))
async def help_command(message: types.Message):
    HELPFUL_REPLY = f"/start– знайомство із ботом" \
                    f"\n/help–допомога" \
                    f"\n/add_task– щоб додати нагадування із справ (щось просте, нап. помити кота)" \
                    f"\n/add_objective– додати ціль на перспективу (накшталт купити автомобіль)" \
                    f"\n/cancel_add– якщо передумали додати ціль" \
                    f"\n/todo_list, /todo, /td– команда виклику списку справ і цілей, щоб отримати незроблені, допишіть todo, для завершених допишіть done, аби побачити всі– пишіть all, за замовчуванням мод– це all"

    await message.answer(HELPFUL_REPLY)


def notifications_times(add_datetime, deadline):
    time_diff = deadline - add_datetime
    notification_times = min(time_diff.days // 3, 3)
    return notification_times

async def notify(aim: models.Model, user_id):
    now = datetime.datetime.now()
    add_datetime, deadline = aim.add_datetime, aim.deadline
    times = notifications_times(add_datetime, deadline)
    for t in range(times):
        period = t/times
        asyncio.sleep((period-now).seconds)
        bot.send_message(user_id, aim.name)


@dp.message(Command(commands=['add_objective']))
async def add_objective_command(message: types.Message, forms: FormsManager):
   await forms.show('objectiveform')


@dp.message(Command(commands=['add_task']))
async def add_task_command(message: types.Message, forms: FormsManager):
   await forms.show('taskform')


@dp.message(Command(commands=['cancel_add']))
async def cancel_add_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('передумали🙃')


@dp.message(Command(commands='todo, todo_list, td'))
async def todo_list_command(message: types.Message, command: CommandObject):
    mode = command.args
    user_id = message.from_user.id

    user_todo_list = await todo_list(user_id, mode)
    await message.answer(user_todo_list)

