# Generated by Django 4.2.5 on 2023-09-24 19:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0169_alter_aboutus_id_alter_additionalcategory_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 5, 1, 10, 7, 858202), verbose_name='Дата конца брони'),
        ),
    ]
