#aiogram
from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
#aiogram

#aiogram_forms
from aiogram_forms import dispatcher as forms_distpatcher
#aiogram_forms

#django
from django.core.exceptions import PermissionDenied
from django.conf import settings
#django


TOKEN = settings.TOKEN

storage = MemoryStorage


bot = Bot(token=TOKEN)
dp = Dispatcher()#storage=storage)
router = Router()
dp.include_router(router)
forms_distpatcher.attach(dp)


