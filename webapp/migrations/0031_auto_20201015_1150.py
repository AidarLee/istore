# Generated by Django 3.1.1 on 2020-10-15 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0030_auto_20201015_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseoncredit',
            name='phone',
            field=models.CharField(max_length=100, verbose_name='Номер телефона'),
        ),
    ]
