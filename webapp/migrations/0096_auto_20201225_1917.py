# Generated by Django 3.1.1 on 2020-12-25 19:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0095_auto_20201225_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankpercents',
            name='months',
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 4, 19, 17, 44, 672477), verbose_name='Дата конца брони'),
        ),
    ]
