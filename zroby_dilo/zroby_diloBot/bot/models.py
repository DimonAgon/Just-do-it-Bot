from django.db import models


class AimType(models.TextChoices):
    OBJECTIVE = 'ціль'
    TASK = 'задача'


class AimStatus(models.TextChoices):
    InPROGRESS = 'in progress'
    DONE = 'done'


class Aim(models.Model):
    name = models.CharField(verbose_name='Назва', max_length=100)
    declaration = models.TextField(verbose_name='Опис', blank=True)
    add_datetime = models.DateTimeField(verbose_name='Час')
    aim_type = models.CharField(verbose_name='Тип', choices=AimType.choices, max_length=6)
    deadline = models.DateTimeField(verbose_name='Дедлайн')
    status = models.CharField(verbose_name='Cтатус', choices=AimStatus.choices, max_length=11)
    external_id = models.IntegerField()
