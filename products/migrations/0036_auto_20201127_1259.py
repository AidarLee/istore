# Generated by Django 3.1.1 on 2020-11-27 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0035_auto_20201112_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Активный'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_category',
            field=models.CharField(choices=[('iphone', 'iPhone '), ('macBook', 'MacBook '), ('iPad', 'iPad'), ('iMac', 'iMac'), ('apple-watch', 'Apple Watch'), ('gadgets', 'Гаджеты'), ('airpods', 'AirPods'), ('accessory', 'Аксеcсуары')], max_length=20, null=True, verbose_name='Категория'),
        ),
    ]
