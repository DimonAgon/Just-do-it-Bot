import asyncio

from .dispatcher import bot
from ..views import aim_done
from ..models import Aim, AimStatus

from typing import Type

import datetime
from django.utils import timezone

def notifications_times(add_datetime, deadline):
    time_diff = deadline - add_datetime
    time_diff_days = time_diff.seconds/3600/24
    notification_times = time_diff_days/3
    return 1 if notification_times <= 1 else 2 if notification_times <= 3 else 3

async def notify(aim: Type[Aim]):
    now = timezone.make_aware(datetime.datetime.now())
    add_datetime, deadline = aim.add_datetime, aim.deadline
    time_difference = deadline - now
    times = notifications_times(add_datetime, deadline)

    if times == 1:
        await asyncio.sleep(time_difference.seconds/2)
        await bot.send_message(aim.external_id, aim.name)


    else:
        for t in range(times):
            await asyncio.sleep(time_difference.seconds/times)
            await bot.send_message(aim.external_id, aim.name)

    await aim_done(aim)