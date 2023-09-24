# Generated by Django 3.1.1 on 2020-10-31 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_remove_module_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='category_name',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Название категории'),
        ),
        migrations.AddField(
            model_name='module',
            name='name',
            field=models.CharField(blank=True, help_text='Нужно для того \n                                                                                                    чтобы два \n                                                                                                    модуля были \n                                                                                                    взаимоисключаемые,\n                                                                                                    слово должно быть \n                                                                                                    без пробелов', max_length=250, null=True, verbose_name='Уникальное слово'),
        ),
    ]
