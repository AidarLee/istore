# Generated by Django 3.1.1 on 2021-11-24 11:09

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0160_auto_20211124_1108'),
    ]

    operations = [
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=600, null=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Контент')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Порядок')),
            ],
            options={
                'verbose_name': 'Футер',
                'verbose_name_plural': 'Футер',
            },
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 4, 11, 9, 34, 54388), verbose_name='Дата конца брони'),
        ),
    ]
