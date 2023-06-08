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
    intro = "start" #TODO: add intro text

    await message.answer(intro)


@dp.message(Command(commands=['help']))
async def help_command(message: types.Message):
    HELPFUL_REPLY = "help" #TODO: add intro text

    await message.answer(HELPFUL_REPLY)


@dp.message(Command(commands=['add_aim']))
async def add_objective_command(message: types.Message, forms: FormsManager):
    aim_type_str = AimType.OBJECTIVE.value
    callback_success_text = f"+ {aim_type_str})"
    callback_fail_text = f"Помилка, {aim_type_str} не вдалося додати("

    try:
        await forms.show(['aimform'])
        data = await forms.get_data(AimForm)
        new_aim(data)
        message.answer(callback_success_text)

    except Exception as e:
        await message.answer(callback_fail_text)
        logging.error(f"aim adding failed, error: {e}")


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

@dp.message(Command(commands=['add_task']))
async def add_task_command(message: types.Message, forms: FormsManager):
    aim_type_str = AimType.TASK.value
    callback_success_text = f"+ {aim_type_str})"
    callback_fail_text = f"Помилка, {aim_type_str} не вдалося додати("

    try:
        await forms.show('aiomform')
        await forms.show('taskdeadlinetime')
        data = await forms.get_data(AimForm)
        deadline_time = await forms.get_data(TaskDeadlineTime)
        new_aim(data, deadline_time)
        message.answer(callback_success_text)

    except Exception as e:
        await message.answer(callback_fail_text)
        logging.error(f"aim adding failed, error: {e}")


@dp.message(Command(commands='todo, todo_list, td'))
async def todo_list_command(message: types.Message, command: CommandObject):
    mode = command.args
    user_id = message.from_user.id

    user_todo_list = await todo_list(user_id, mode)
    await message.answer(user_todo_list)

