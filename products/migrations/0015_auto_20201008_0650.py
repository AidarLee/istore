# Generated by Django 3.1.1 on 2020-10-08 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_product_additional_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='additional_category',
            field=models.CharField(choices=[('apple-tv', 'Apple TV '), ('сables-and-adapters', 'Кабели и переходники '), ('keyboards-and-mice', 'Клавиатуры и мышки'), ('charging-device', 'Зарядные устройства'), ('headphones-and-speakers', 'Наушники и колонки'), ('cases-and-bags', 'Чехлы и сумки')], max_length=30, null=True, verbose_name='Подкатегория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_category',
            field=models.CharField(choices=[('iphone', 'iPhone '), ('mackBook', 'MacBook '), ('iPad', 'iPad'), ('iMac', 'iMac'), ('apple-watch', 'Apple Watch'), ('gadgets', 'Гаджеты'), ('airpods', 'AirPods'), ('accessory', 'Акссесуары')], max_length=20, null=True, verbose_name='Категория'),
        ),
        migrations.CreateModel(
            name='MainSpecification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='specification', verbose_name='Изображение')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_spec', to='products.product')),
            ],
            options={
                'verbose_name': 'Основную характеристику',
                'verbose_name_plural': 'Основные характеристики',
            },
        ),
    ]
