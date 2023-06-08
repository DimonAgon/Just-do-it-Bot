

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
    pass


@dispatcher.register('aimform')
class AimForm(Form):
    name = fields.TextField("Напишіть назву цілі")
    declaration = fields.TextField("Опишіть ціль")
    deadline = fields.TextField("Який дедлайн за датою?", validators=[validate_date_format])

@dispatcher.register('taskdeadlinetime')
class TaskDeadlineTime(Form):
    deadline_time = fields.TextField("О котрій?", validators=[validate_time_format])