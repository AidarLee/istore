# Generated by Django 3.1.1 on 2021-09-24 00:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0124_auto_20210921_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 4, 0, 41, 9, 82067), verbose_name='Дата конца брони'),
        ),
    ]
