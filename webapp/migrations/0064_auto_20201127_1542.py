# Generated by Django 3.1.1 on 2020-11-27 15:42

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0063_auto_20201127_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainPageSlider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Контент')),
                ('category', models.CharField(blank=True, choices=[('1', 'Главная'), ('2', 'Акционная')], max_length=30, null=True, verbose_name='Категория')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Слайдер',
                'verbose_name_plural': 'Слайдеры',
            },
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 7, 15, 42, 17, 515976), verbose_name='Дата конца брони'),
        ),
    ]
