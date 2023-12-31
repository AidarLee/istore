# Generated by Django 3.1.1 on 2020-10-13 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0023_bank'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='loan_desc',
            field=models.TextField(default=100, verbose_name='Описание покупки в кредит'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='settings',
            name='loan_title',
            field=models.CharField(default=100, max_length=400, verbose_name='Текст покупки в кредит'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bank',
            name='img',
            field=models.ImageField(upload_to='banks', verbose_name='Лого'),
        ),
    ]
