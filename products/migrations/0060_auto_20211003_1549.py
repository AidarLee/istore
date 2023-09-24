# Generated by Django 3.1.1 on 2021-10-03 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0059_auto_20210926_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productspecification',
            name='connectivity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='connectivity', to='products.connectivity', verbose_name='Возможности подключения'),
        ),
    ]