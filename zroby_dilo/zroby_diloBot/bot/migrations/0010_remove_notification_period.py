# Generated by Django 4.2.2 on 2023-06-12 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0009_remove_aim_times_notified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='period',
        ),
    ]