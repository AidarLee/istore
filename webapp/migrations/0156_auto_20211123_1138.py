# Generated by Django 3.1.1 on 2021-11-23 11:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0065_auto_20211003_2307'),
        ('webapp', '0155_auto_20211012_2318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compare',
            name='products',
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 3, 11, 38, 12, 899834), verbose_name='Дата конца брони'),
        ),
        migrations.CreateModel(
            name='CompareProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Порядок')),
                ('compare', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.compare')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Сравнение',
                'verbose_name_plural': 'Сравнения',
            },
        ),
    ]