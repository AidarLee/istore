# Generated by Django 3.1.1 on 2020-10-30 15:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0048_auto_20201021_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='facebook',
            field=models.CharField(default=1, max_length=400, verbose_name='Ссылка на facebook'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='settings',
            name='instagram',
            field=models.CharField(default=1, max_length=400, verbose_name='Ссылка на instagram'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 9, 15, 17, 42, 383187), verbose_name='Дата конца брони'),
        ),
    ]