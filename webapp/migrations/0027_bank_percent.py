# Generated by Django 3.1.1 on 2020-10-14 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0026_auto_20201014_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='percent',
            field=models.IntegerField(default=1, verbose_name='Процент'),
            preserve_default=False,
        ),
    ]
