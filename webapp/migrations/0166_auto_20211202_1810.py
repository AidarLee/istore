# Generated by Django 3.1.1 on 2021-12-02 18:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0165_auto_20211202_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 12, 18, 10, 45, 378008), verbose_name='Дата конца брони'),
        ),
    ]
