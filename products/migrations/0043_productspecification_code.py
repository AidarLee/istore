# Generated by Django 3.1.1 on 2021-07-29 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0042_auto_20210311_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='productspecification',
            name='code',
            field=models.TextField(blank=True, null=True, verbose_name='УКТ'),
        ),
    ]
