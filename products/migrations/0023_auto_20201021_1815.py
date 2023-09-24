# Generated by Django 3.1.1 on 2020-10-21 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0022_auto_20201021_1808'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='capacity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='color',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='capacity',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Ёмкость'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='color',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Цвет'),
        ),
    ]
