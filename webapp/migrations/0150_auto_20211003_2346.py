# Generated by Django 3.1.1 on 2021-10-03 23:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0149_auto_20211003_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpage',
            name='page_description',
            field=models.TextField(blank=True, null=True, verbose_name='Meta Description'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 13, 23, 46, 30, 376052), verbose_name='Дата конца брони'),
        ),
    ]
