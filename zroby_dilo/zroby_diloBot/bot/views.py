import datetime

from typing import Type

from .models import *
from .infrastructure.enums import *

from channels.db import database_sync_to_async

from django.utils import timezone

from itertools import repeat, chain


@database_sync_to_async
def new_aim(data, user_id):
    initial = {}
    initial['name'], initial['declaration'] = data['name'], data['declaration']
    deadline_date_formated = datetime.datetime.strptime(data['deadline_date'], '%d.%m.%Y').date()
    deadline_time_formated = datetime.datetime.strptime(data['deadline_time'], '%H:%M').time()
    deadline = timezone.make_aware(datetime.datetime.combine(deadline_date_formated, deadline_time_formated))
    initial['deadline'] = deadline
    initial['status'] = AimStatus.InPROGRESS
    initial['external_id'] = user_id
    aim = Aim.objects.create(**initial)
    aim.save()

    return aim


@database_sync_to_async
def aim_done(aim: Type[Aim]):
    aim.status = AimStatus.DONE
    aim.save()

def aims_to_list(query):
    list_ = ""
    for aim in query:
        if aim.status == AimStatus.InPROGRESS:
            list_ += aim.name + '\n'
        else:
            list_ += f"\u0336{aim.name}\u0336"
            list_ += '\n'

    return list_



@database_sync_to_async
def todo_list(user_id, mode=TodoListModes.TODO):
    user_aims = Aim.objects.filter(external_id=user_id)
    match TodoListModes(mode):
        case TodoListModes.ALL: #TODO: fix modes
            aims = user_aims

        case TodoListModes.TODO:
            aims = user_aims.filter(status=AimStatus.InPROGRESS)

        case TodoListModes.DONE:
            aims = user_aims.filter(status=AimStatus.DONE)

    return aims_to_list(aims)