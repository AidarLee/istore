# Generated by Django 3.1.1 on 2020-10-05 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to='documents/%Y-%m-%d'),
        ),
    ]
