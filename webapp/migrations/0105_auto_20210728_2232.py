# Generated by Django 3.1.1 on 2021-07-28 22:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0104_auto_20210311_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 7, 22, 32, 10, 759606), verbose_name='Дата конца брони'),
        ),
    ]
