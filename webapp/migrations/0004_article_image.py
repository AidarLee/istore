# Generated by Django 3.1.1 on 2020-09-28 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20200928_0506'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='articles', verbose_name='Изображение'),
        ),
    ]
