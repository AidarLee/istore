# Generated by Django 3.1.1 on 2020-10-01 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_callback'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CallBack',
            new_name='ServiceCallBack',
        ),
    ]
