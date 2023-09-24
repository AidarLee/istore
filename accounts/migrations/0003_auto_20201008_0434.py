# Generated by Django 3.1.1 on 2020-10-08 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20201007_0856'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('accounts', '0002_profile_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='password',
            field=models.CharField(blank=True, help_text='Пароль зашифрован, его можно только изменить', max_length=250, null=True, verbose_name='Пароль'),
        ),
        migrations.DeleteModel(
            name='ProfileAdmin',
        ),
    ]