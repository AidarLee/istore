# Generated by Django 3.1.1 on 2020-12-18 16:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0084_auto_20201218_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 28, 16, 2, 56, 299379), verbose_name='Дата конца брони'),
        ),
    ]
