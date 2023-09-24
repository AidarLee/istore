# Generated by Django 3.1.1 on 2020-11-27 12:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0061_auto_20201116_1428'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Изображение Категории', 'verbose_name_plural': 'Изображение Категорий'},
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 7, 12, 59, 25, 707689), verbose_name='Дата конца брони'),
        ),
    ]
