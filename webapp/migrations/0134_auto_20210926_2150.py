# Generated by Django 3.1.1 on 2021-09-26 21:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0133_auto_20210926_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 6, 21, 50, 10, 954228), verbose_name='Дата конца брони'),
        ),
    ]
