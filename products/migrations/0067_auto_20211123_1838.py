# Generated by Django 3.1.1 on 2021-11-23 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0066_product_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='seo_desc',
            field=models.TextField(blank=True, null=True, verbose_name='SEO описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание продукта'),
        ),
    ]