# Generated by Django 3.1.1 on 2020-11-27 18:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0065_auto_20201127_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpageslider',
            name='title',
            field=models.CharField(blank=True, max_length=600, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 7, 18, 1, 2, 674206), verbose_name='Дата конца брони'),
        ),
    ]
