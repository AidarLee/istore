# Generated by Django 3.1.1 on 2020-12-25 11:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0093_auto_20201224_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankpercents',
            name='months',
            field=models.IntegerField(blank=True, null=True, verbose_name='Месяц'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 4, 11, 22, 35, 722381), verbose_name='Дата конца брони'),
        ),
    ]
