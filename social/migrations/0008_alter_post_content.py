# Generated by Django 3.2.9 on 2021-11-27 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_auto_20211123_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.FileField(blank=True, null=True, upload_to='media/posts'),
        ),
    ]