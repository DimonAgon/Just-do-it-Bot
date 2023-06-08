
from .models import *
from .infrastructure.enums import *
from channels.db import database_sync_to_async


@database_sync_to_async
def new_aim(aim_type, data, deadline_time):
    initial = data
    initial['aim_type'] = aim_type
    aim = Aim.objects.create(**initial)
    aim.save()

    return aim


@database_sync_to_async
def todo_list(user_id, mode):
    user_aims = Aim.objects.get(external_id=user_id)
    match mode:
        case TodoListModes.ALL:
            return user_aims

        case TodoListModes.TODO:
            todo_aims = user_aims#filter by status='in_progress'
            return todo_aims

        case TodoListModes.DONE:
            done_aims = user_aims#filter by status='done'
            return done_aims

