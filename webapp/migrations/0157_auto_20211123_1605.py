# Generated by Django 3.1.1 on 2021-11-23 16:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0156_auto_20211123_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compareproducts',
            name='compare',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='compare_product', to='webapp.compare'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 3, 16, 5, 41, 683104), verbose_name='Дата конца брони'),
        ),
    ]
