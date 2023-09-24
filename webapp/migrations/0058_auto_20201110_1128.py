# Generated by Django 3.1.1 on 2020-11-10 11:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0057_auto_20201102_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='email',
            field=models.CharField(default=1, max_length=400, verbose_name='Email почта'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 20, 11, 28, 16, 200486), verbose_name='Дата конца брони'),
        ),
    ]