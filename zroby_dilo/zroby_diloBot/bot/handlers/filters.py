import aiogram
from aiogram.filters import BaseFilter, CommandObject
from aiogram import types

from typing import Type

from django.db import models

from channels.db import database_sync_to_async

from .dispatcher import bot

import logging

from django.core.exceptions import ValidationError

from enum import Enum

import datetime

from ..infrastructure.enums import *


no_mode_validation_error_message = "Помилка, вкажіть режим"

wrong_mode_validation_error_message = "Помилка, вказано невірний режим"

no_arguments_validation_error_message = "Помилка, вкажіть аргументи"

wrong_lessons_validation_error_mesage = "Помилка, очікується послідовність занять"

wrong_date_validation_error_message = "Помилка, очікується дата"


def aftercommand_check(value):
    if value:
        return True

    raise ValidationError("Command initiation failed\nError: no arguments", code='arguments')


def validate_is_mode(value, modes: Enum):

    mode = next((mode for mode in modes if mode.value == value), None)

    if mode:
        return  True

    raise ValidationError(f"Command initiation failed\nError:no such mode \"{value}\"", code='arguments')


class AdditionalArgumentsValidator:
    def __init__(self, validation_function, validation_error_message):
        self.validation_function = validation_function
        self.validation_error_message = validation_error_message


class NativeDateFormat:
    date_format = '%d.%m.%Y'

def validate_date_format(value):
    date_format = NativeDateFormat.date_format

    try:
        datetime.datetime.strptime(value, date_format).date()
        return

    except:
        raise ValidationError("wrong date format", code='format')

date_validator = AdditionalArgumentsValidator(validate_date_format, wrong_date_validation_error_message)



class AftercommandFullCheck(BaseFilter):
    key = 'aftercommand'

    def __init__(self, allow_no_argument: bool, modes: Enum, mode_checking=False,
                 additional_arguments_checker: Type[AdditionalArgumentsValidator]=None,
                 flag_checking=False):
        self.allow_no_argument = allow_no_argument
        self.modes = modes
        self.mode_checking = mode_checking
        self.additional_arguments_checker = additional_arguments_checker
        self.flag_checking = flag_checking
    async def __call__(self, message: types.Message, command: CommandObject) -> bool:
        aftercommand = command.args

        try: aftercommand_check(aftercommand)
        except:
            if self.allow_no_argument:
                return True

            await message.answer(no_arguments_validation_error_message)
            return False

        arguments = aftercommand.split()

        if self.mode_checking and self.additional_arguments_checker and self.flag_checking:
            pseudo_mode, *additional_arguments, pseudo_flag = arguments

        elif self.mode_checking and self.additional_arguments_checker:
            pseudo_mode, *additional_arguments = arguments

        elif self.mode_checking and self.flag_checking:
            pseudo_mode, pseudo_flag = arguments

        elif self.additional_arguments_checker and self.flag_checking:
            *additional_arguments, pseudo_flag = arguments

        elif self.mode_checking:
            pseudo_mode = arguments[0]

        elif self.additional_arguments_checker:
            additional_arguments = arguments

        elif self.flag_checking:
            pseudo_flag = arguments[0]

        if self.mode_checking:
            try: pseudo_mode
            except:
                await message.answer(no_mode_validation_error_message)
                return False

            try: validate_is_mode(pseudo_mode, self.modes)
            except:
                try:
                    self.additional_arguments_checker.validation_function(pseudo_mode)
                    additional_argument = pseudo_mode
                    additional_arguments.insert(0, additional_argument)

                except:
                    await message.answer(wrong_mode_validation_error_message)
                    return False

        if self.flag_checking:
            try: validate_is_mode(pseudo_flag, self.modes.Flag)
            except:
                try:
                    self.additional_arguments_checker.validation_function(pseudo_flag)
                    additional_argument = pseudo_flag
                    additional_arguments.append(additional_argument)

                except:
                    await message.answer(wrong_mode_validation_error_message)
                    return False

        if self.additional_arguments_checker:
            if not additional_arguments:
                await message.answer(self.additional_arguments_checker.validation_error_message)
                return False

            try:
                for i in additional_arguments:
                    self.additional_arguments_checker.validation_function(i)
            except:
                await message.answer(self.additional_arguments_checker.validation_error_message)
                return False

        return True
