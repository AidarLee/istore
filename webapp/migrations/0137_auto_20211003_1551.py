# Generated by Django 3.1.1 on 2021-10-03 15:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0136_auto_20211003_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 13, 15, 51, 4, 84922), verbose_name='Дата конца брони'),
        ),
    ]
