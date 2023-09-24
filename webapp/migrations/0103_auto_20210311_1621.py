# Generated by Django 3.1.1 on 2021-03-11 16:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0102_auto_20210311_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='accessory_4',
            field=models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Доп. Акссесуары 4'),
        ),
        migrations.AddField(
            model_name='category',
            name='accessory_4_on',
            field=models.BooleanField(default=False, verbose_name='Доп. Акссесуары 4 включить'),
        ),
        migrations.AddField(
            model_name='category',
            name='accessory_4_title',
            field=models.TextField(blank=True, null=True, verbose_name='Доп. Акссесуары 4 название'),
        ),
        migrations.AddField(
            model_name='category',
            name='gadget_4',
            field=models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Доп. Гаджеты 4'),
        ),
        migrations.AddField(
            model_name='category',
            name='gadget_4_on',
            field=models.BooleanField(default=False, verbose_name='Доп. Гаджеты 4 включить'),
        ),
        migrations.AddField(
            model_name='category',
            name='gadget_4_title',
            field=models.TextField(blank=True, null=True, verbose_name='Доп. Гаджеты 4 название'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 21, 16, 21, 20, 379174), verbose_name='Дата конца брони'),
        ),
    ]
