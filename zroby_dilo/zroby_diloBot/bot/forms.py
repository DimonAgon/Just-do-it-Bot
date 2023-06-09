

import logging

from aiogram import types

from aiogram_forms import dispatcher, Form, FormsManager, fields
from aiogram_forms.errors import ValidationError

from .views import *

import datetime


def validate_date_format(value):
    date_format = '%d.%m.%Y'

    try:
        datetime.datetime.strptime(value, date_format).date()
        return value

    except:
        raise ValidationError("wrong date format", code='format_match')

def validate_time_format(value):
    time_format = '%H:%M'

    try:
        datetime.datetime.strptime(value, time_format).time()
        return value

    except ValueError:
        raise ValidationError("Wrong time format", code='format_match')

name_field = fields.TextField("Напишіть назву цілі")
declaration_field = fields.TextField("Опишіть ціль")
deadline_date_field = fields.TextField("Який дедлайн за датою?", validators=[validate_date_format])


@dispatcher.register('objectiveform')
class ObjectiveForm(Form):
    name = name_field
    declaration = declaration_field
    deadline_date = deadline_date_field

    @classmethod
    async def callback(cls, message: types.Message, forms: FormsManager, **data) -> None:
        aim_type_str = AimType.OBJECTIVE.value
        callback_success_text = f"+ {aim_type_str})"
        callback_fail_text = f"Помилка, {aim_type_str} не вдалося додати("

        try:
            data = await forms.get_data(ObjectiveForm)
            await new_aim(AimType.OBJECTIVE, data)
            await message.answer(callback_success_text)

        except Exception as e:
            await message.answer(callback_fail_text)
            logging.error(f"aim adding failed, error: {e}")




@dispatcher.register('taskform')
class TaskForm(Form):
    name = name_field
    declaration = declaration_field
    deadline_date = deadline_date_field
    deadline_time = fields.TextField("О котрій?", validators=[validate_time_format])

    @classmethod
    async def callback(cls, message: types.Message, forms: FormsManager, **data) -> None:
        aim_type_str = AimType.TASK.value
        callback_success_text = f"+ {aim_type_str})"
        callback_fail_text = f"Помилка, {aim_type_str} не вдалося додати("

        try:
            data = await forms.get_data(TaskForm)
            await new_aim(AimType.TASK, data)
            await message.answer(callback_success_text)

        except Exception as e:
            await message.answer(callback_fail_text)
            logging.error(f"aim adding failed, error: {e}")