# Generated by Django 3.1.1 on 2021-10-03 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0146_auto_20211003_2307'),
        ('products', '0063_remove_orderproduct_module'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='additional_category',
        ),
        migrations.AddField(
            model_name='product',
            name='second_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='add_category', to='webapp.additionalcategory', verbose_name='Подкатегория'),
        ),
    ]
