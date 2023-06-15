import asyncio
import logging

from .dispatcher import bot
from ..models import Aim, AimStatus, Notification

from typing import Type

import datetime
from django.utils import timezone

from channels.db import database_sync_to_async


class Notifier:

    @database_sync_to_async
    def remove_fatigued_notifications(self, notification_queue):
        for notification in notification_queue:
            aim = notification.aim

            notification.delete()

            if not Notification.objects.filter(aim=aim):
                aim.status = AimStatus.DONE
                aim.save()


    @classmethod
    async def notify(cls, notification_queue):
        for notification in notification_queue:
            user_id = notification.aim.external_id
            await bot.send_message(user_id, notification.aim.name)
            logging.info(f'notfication {notification.id} sent to {user_id}')


    @database_sync_to_async
    def notifications_queue(self):
        now = timezone.make_aware(datetime.datetime.now())
        notifications = Notification.objects.all()
        nq = []

        for notification in notifications:

            if notification.notify_datetime <= now:
                aim = notification.aim
                nq.append(notification)


        return nq


    @classmethod
    async def track(cls):
        while True:
            await asyncio.sleep(59.99)
            nq = await cls.notifications_queue()
            await cls.notify(nq)
            await cls.remove_fatigued_notifications(nq)


