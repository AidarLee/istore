# Generated by Django 3.1.1 on 2021-09-24 00:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0052_auto_20210921_2316'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casesize',
            options={'verbose_name': 'Размер корпуса', 'verbose_name_plural': 'Размеры корпуса'},
        ),
        migrations.AlterModelOptions(
            name='connectivity',
            options={'verbose_name': 'Возможность подключения', 'verbose_name_plural': 'Возможности подключения'},
        ),
        migrations.AlterModelOptions(
            name='cpu',
            options={'verbose_name': 'Процессор', 'verbose_name_plural': 'Процессор'},
        ),
        migrations.AlterModelOptions(
            name='keyboard',
            options={'verbose_name': 'Раскладка клавиатуры', 'verbose_name_plural': 'Раскладка клавиатуры'},
        ),
        migrations.AlterModelOptions(
            name='pattern',
            options={'verbose_name': 'Модель', 'verbose_name_plural': 'Модель'},
        ),
        migrations.AlterModelOptions(
            name='ram',
            options={'verbose_name': 'Оперативная память', 'verbose_name_plural': 'Оперативная память'},
        ),
        migrations.AddField(
            model_name='productspecification',
            name='images',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Изображении'),
        ),
        migrations.AlterField(
            model_name='productspecification',
            name='cpu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cpu', to='products.cpu', verbose_name='Процессор'),
        ),
        migrations.AlterField(
            model_name='productspecification',
            name='edition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='edition', to='products.edition', verbose_name='Edition'),
        ),
        migrations.AlterField(
            model_name='productspecification',
            name='pattern',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pattern', to='products.pattern', verbose_name='Модель'),
        ),
        migrations.AlterField(
            model_name='productspecification',
            name='ram',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ram', to='products.ram', verbose_name='Оперативная память'),
        ),
    ]
