# Generated by Django 3.1.1 on 2020-12-23 16:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0088_auto_20201223_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bank',
            name='percent',
        ),
        migrations.RemoveField(
            model_name='bank',
            name='percent2',
        ),
        migrations.RemoveField(
            model_name='bank',
            name='percent3',
        ),
        migrations.RemoveField(
            model_name='bank',
            name='percent4',
        ),
        migrations.RemoveField(
            model_name='bank',
            name='percent5',
        ),
        migrations.RemoveField(
            model_name='bank',
            name='percent6',
        ),
        migrations.RemoveField(
            model_name='bank',
            name='percent_before',
        ),
        migrations.RemoveField(
            model_name='bank',
            name='percent_before2',
        ),
        migrations.RemoveField(
            model_name='bank',
            name='percent_before3',
        ),
        migrations.RemoveField(
            model_name='bank',
            name='percent_before4',
        ),
        migrations.RemoveField(
            model_name='bank',
            name='percent_before5',
        ),
        migrations.RemoveField(
            model_name='bank',
            name='percent_before6',
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 2, 16, 49, 7, 762431), verbose_name='Дата конца брони'),
        ),
        migrations.CreateModel(
            name='BankPercents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.FloatField(verbose_name='Процент')),
                ('percent_before', models.FloatField(blank=True, null=True, verbose_name='Процент до достижение суммы')),
                ('bank', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bank', to='webapp.bank')),
            ],
            options={
                'verbose_name': 'Процент банка',
                'verbose_name_plural': 'Проценты банка',
            },
        ),
    ]
