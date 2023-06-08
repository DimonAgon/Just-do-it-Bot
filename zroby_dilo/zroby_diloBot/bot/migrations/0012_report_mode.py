# Generated by Django 4.1.2 on 2023-05-11 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0011_alter_report_lessons'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='mode',
            field=models.CharField(choices=[('L', 'light'), ('N', 'normal'), ('H', 'hardcore'), ('schedule', 'Schedule Mode'), ('zoom', 'Zoom Mode')], default='N', max_length=12),
        ),
    ]