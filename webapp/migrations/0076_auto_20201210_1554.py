# Generated by Django 3.1.1 on 2020-12-10 15:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0075_auto_20201210_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='option',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Оплата через'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 20, 15, 54, 43, 842311), verbose_name='Дата конца брони'),
        ),
    ]
