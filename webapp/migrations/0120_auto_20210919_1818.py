# Generated by Django 3.1.1 on 2021-09-19 18:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0119_auto_20210812_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 29, 18, 18, 22, 759315), verbose_name='Дата конца брони'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Номер транзакции'),
        ),
    ]
