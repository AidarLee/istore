# Generated by Django 4.2.5 on 2023-09-25 09:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0171_alter_reserve_last_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 5, 9, 43, 3, 643529), verbose_name='Дата конца брони'),
        ),
    ]
