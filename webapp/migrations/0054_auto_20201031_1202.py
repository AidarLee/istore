# Generated by Django 3.1.1 on 2020-10-31 12:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0053_auto_20201030_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 10, 12, 2, 47, 577534), verbose_name='Дата конца брони'),
        ),
    ]
