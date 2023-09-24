# Generated by Django 3.1.1 on 2020-12-18 15:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0083_auto_20201218_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanpage',
            name='text_22',
            field=models.CharField(blank=True, max_length=600, null=True, verbose_name='Необходимые документы'),
        ),
        migrations.AddField(
            model_name='loanpage',
            name='text_23',
            field=models.CharField(blank=True, max_length=600, null=True, verbose_name='Оформление кредита в нашем офисе'),
        ),
        migrations.AlterField(
            model_name='loanpage',
            name='title_2',
            field=models.CharField(blank=True, max_length=600, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 28, 15, 45, 17, 875551), verbose_name='Дата конца брони'),
        ),
    ]
