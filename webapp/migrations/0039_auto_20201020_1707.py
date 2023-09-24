# Generated by Django 3.1.1 on 2020-10-20 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0038_reserve_reserve_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='capacity',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Ёмкость'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='color',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='payment',
            field=models.FloatField(blank=True, max_length=100, null=True, verbose_name='Сумма брони'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='phone',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Контактный номер'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='price',
            field=models.FloatField(blank=True, null=True, verbose_name='Цена устройства на момент брони'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='price_converted',
            field=models.FloatField(blank=True, null=True, verbose_name='Цена устройства в сомах'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='reserve_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Цена брони'),
        ),
    ]
