# Generated by Django 3.1.1 on 2020-10-21 18:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0040_auto_20201021_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 31, 18, 8, 3, 265410), verbose_name='Дата конца брони'),
        ),
    ]
