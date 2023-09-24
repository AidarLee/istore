# Generated by Django 3.1.1 on 2020-11-16 14:28

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0060_auto_20201112_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Mac изображение')),
                ('iphone', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='iPhone изображение')),
                ('ipad', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='iPad изображение')),
                ('watch', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Watch изображение')),
                ('accessory', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Аксессуары изображение')),
                ('gadget', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Гаджеты изображение')),
                ('cable', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Кабели изображение')),
                ('charge', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Адаптеры изображение')),
                ('keyboard', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Клавиатуры и мышки изображение')),
                ('speaker', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Колонки изображение')),
                ('cases', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Чехлы изображение')),
                ('adapter', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Переходники изображение')),
                ('stylus', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Стилусы изображение')),
                ('protective', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Защитные стекла изображение')),
                ('drone', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Дроны изображение')),
                ('tv', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Приставки изображение')),
                ('stabilizer', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Стабилизаторы изображение')),
                ('camera', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Камеры изображение')),
                ('garmin', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Garmin изображение')),
                ('vr', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='VR очки изображение')),
                ('tablets', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Графические планшеты изображение')),
                ('another', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Разное изображение')),
                ('trade_iphone', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Trade - in iPhone изображение')),
                ('trade_ipad', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Trade - in iPad изображение')),
                ('trade_mac', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Trade - in MacBook изображение')),
                ('trade_watch', models.ImageField(blank=True, null=True, upload_to='category', verbose_name='Trade - in Apple Watch изображение')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Страница о нас',
                'verbose_name_plural': 'Страница о нас',
            },
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 26, 14, 28, 35, 450553), verbose_name='Дата конца брони'),
        ),
    ]
