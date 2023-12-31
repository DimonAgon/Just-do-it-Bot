# Generated by Django 4.2.2 on 2023-06-12 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_aim_times_notified_delete_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notify_datetime', models.DateTimeField(verbose_name='Час нагадування')),
                ('period', models.IntegerField(verbose_name='Таке нагадування за рахунком')),
                ('aim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.aim', verbose_name='Ціль')),
            ],
        ),
    ]
