# Generated by Django 3.1.1 on 2021-10-03 23:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0146_auto_20211003_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 13, 23, 7, 37, 664813), verbose_name='Дата конца брони'),
        ),
    ]
