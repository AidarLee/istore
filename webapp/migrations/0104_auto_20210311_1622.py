# Generated by Django 3.1.1 on 2021-03-11 16:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0103_auto_20210311_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='accessory_5',
            field=models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Доп. Акссесуары 5'),
        ),
        migrations.AddField(
            model_name='category',
            name='accessory_5_on',
            field=models.BooleanField(default=False, verbose_name='Доп. Акссесуары 5 включить'),
        ),
        migrations.AddField(
            model_name='category',
            name='accessory_5_title',
            field=models.TextField(blank=True, null=True, verbose_name='Доп. Акссесуары 5 название'),
        ),
        migrations.AddField(
            model_name='category',
            name='gadget_5',
            field=models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Доп. Гаджеты 5'),
        ),
        migrations.AddField(
            model_name='category',
            name='gadget_5_on',
            field=models.BooleanField(default=False, verbose_name='Доп. Гаджеты 5 включить'),
        ),
        migrations.AddField(
            model_name='category',
            name='gadget_5_title',
            field=models.TextField(blank=True, null=True, verbose_name='Доп. Гаджеты 5 название'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 21, 16, 22, 42, 168874), verbose_name='Дата конца брони'),
        ),
    ]