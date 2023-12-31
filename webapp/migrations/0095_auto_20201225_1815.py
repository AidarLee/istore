# Generated by Django 3.1.1 on 2020-12-25 18:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0094_auto_20201225_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseoncreditproducts',
            name='bank',
        ),
        migrations.RemoveField(
            model_name='purchaseoncreditproducts',
            name='month',
        ),
        migrations.RemoveField(
            model_name='purchaseoncreditproducts',
            name='per_month',
        ),
        migrations.AddField(
            model_name='purchaseoncredit',
            name='bank',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Банк'),
        ),
        migrations.AddField(
            model_name='purchaseoncredit',
            name='month',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Срок кредита'),
        ),
        migrations.AddField(
            model_name='purchaseoncredit',
            name='per_month',
            field=models.FloatField(blank=True, null=True, verbose_name='Оплата в месяц'),
        ),
        migrations.AddField(
            model_name='purchaseoncredit',
            name='whole_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Общая сумма'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 4, 18, 15, 29, 754502), verbose_name='Дата конца брони'),
        ),
    ]
