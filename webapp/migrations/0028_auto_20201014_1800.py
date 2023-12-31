# Generated by Django 3.1.1 on 2020-10-14 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0027_bank_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='initial_fee_before',
            field=models.IntegerField(verbose_name='Первоначальный взнос после'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='percent',
            field=models.FloatField(verbose_name='Процент'),
        ),
    ]
