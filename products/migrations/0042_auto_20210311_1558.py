# Generated by Django 3.1.1 on 2021-03-11 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0041_product_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='additional_category',
            field=models.CharField(blank=True, choices=[('apple-tv', 'Apple TV '), ('cables', 'Кабели'), ('adapters', 'Переходники'), ('protective-glass', 'Защитные стекла'), ('stylus', 'Стилусы'), ('keyboards-and-mouse', 'Клавиатуры и мышки'), ('charging-device', 'Зарядные устройства'), ('headphones-and-speakers', 'Наушники и колонки'), ('cases-and-bags', 'Чехлы и сумки'), ('drones', 'Дроны'), ('stabilizers', 'Стабилизаторы'), ('camera', 'Камеры'), ('garmin', 'Garmin'), ('vr-glasses', 'VR  очки'), ('graphic-tablets', 'Графические планшеты'), ('another', 'Разное'), ('mac-16', 'MacBook Pro 16'), ('mac-13', 'MacBook Pro 13'), ('mac-13-air', 'MacBook Air 13'), ('mac-12', 'MacBook Retina 12'), ('mac-mini', 'Mac mini'), ('mac-pro', 'Mac Pro'), ('accessory_1', 'Доп Аксессуары 1'), ('accessory_2', 'Доп Аксессуары 2'), ('accessory_3', 'Доп Аксессуары 3'), ('accessory_4', 'Доп Аксессуары 4'), ('accessory_5', 'Доп Аксессуары 5'), ('gadget_1', 'Доп Гаджеты 1'), ('gadget_2', 'Доп Гаджеты 2'), ('gadget_3', 'Доп Гаджеты 3'), ('gadget_4', 'Доп Гаджеты 4'), ('gadget_5', 'Доп Гаджеты 5')], max_length=30, null=True, verbose_name='Подкатегория'),
        ),
    ]