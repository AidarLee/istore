# Generated by Django 3.1.1 on 2020-10-08 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0015_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='callback',
            name='formalized',
            field=models.BooleanField(default=False, verbose_name='Расмотрен'),
        ),
        migrations.AddField(
            model_name='servicecallback',
            name='formalized',
            field=models.BooleanField(default=False, verbose_name='Расмотрен'),
        ),
    ]
