# Generated by Django 3.1.1 on 2020-10-08 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20201007_0856'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='additional_category',
            field=models.CharField(choices=[('apple_tv', 'Apple TV '), ('сables-and-adapters', 'Кабели и переходники '), ('keyboards-and-mice', 'Клавиатуры и мышки'), ('charging-device', 'Зарядные устройства'), ('headphones-and-speakers', 'Наушники и колонки'), ('cases-and-bags', 'Чехлы и сумки')], max_length=30, null=True, verbose_name='Подкатегория'),
        ),
    ]
