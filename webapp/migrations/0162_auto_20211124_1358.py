# Generated by Django 3.1.1 on 2021-11-24 13:58

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0161_auto_20211124_1109'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=600, null=True, verbose_name='Название')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('contact', models.CharField(blank=True, max_length=600, null=True, verbose_name='Контакты')),
                ('form', models.CharField(blank=True, max_length=600, null=True, verbose_name='Форма обратной связи')),
                ('phone', models.CharField(blank=True, max_length=600, null=True, verbose_name='Номера')),
                ('email', models.CharField(blank=True, max_length=600, null=True, verbose_name='Почта')),
                ('schedule', models.CharField(blank=True, max_length=600, null=True, verbose_name='График')),
                ('socials', models.CharField(blank=True, max_length=600, null=True, verbose_name='Соц сети')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Футер',
                'verbose_name_plural': 'Футер',
            },
        ),
        migrations.RemoveField(
            model_name='footer',
            name='order',
        ),
        migrations.RemoveField(
            model_name='footer',
            name='title',
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 4, 13, 58, 42, 109996), verbose_name='Дата конца брони'),
        ),
    ]