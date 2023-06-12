from django.db import models


class AimStatus(models.TextChoices):
    InPROGRESS = 'in progress'
    DONE = 'done'


class Aim(models.Model):
    name = models.CharField(verbose_name='Назва', max_length=100)
    declaration = models.TextField(verbose_name='Опис', blank=True)
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Початок цілі')
    deadline = models.DateTimeField(verbose_name='Дедлайн')
    status = models.CharField(verbose_name='Cтатус', choices=AimStatus.choices, max_length=11)
    external_id = models.IntegerField()
