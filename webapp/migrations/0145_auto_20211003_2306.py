# Generated by Django 3.1.1 on 2021-10-03 23:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0144_auto_20211003_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 13, 23, 6, 0, 88035), verbose_name='Дата конца брони'),
        ),
    ]