# Generated by Django 3.2.9 on 2022-01-20 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0015_auto_20211201_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='threadmodel',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='threadmodel',
            name='user',
        ),
        migrations.DeleteModel(
            name='MessageModel',
        ),
        migrations.DeleteModel(
            name='ThreadModel',
        ),
    ]
