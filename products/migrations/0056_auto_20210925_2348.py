# Generated by Django 3.1.1 on 2021-09-25 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0055_auto_20210924_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='specification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='products.productspecification'),
        ),
    ]
