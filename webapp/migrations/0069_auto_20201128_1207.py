# Generated by Django 3.1.1 on 2020-11-28 12:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0068_auto_20201128_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 8, 12, 7, 45, 831847), verbose_name='Дата конца брони'),
        ),
    ]