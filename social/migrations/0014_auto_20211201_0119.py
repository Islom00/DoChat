# Generated by Django 3.2.9 on 2021-11-30 20:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0013_delete_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_at', '-shared_at']},
        ),
        migrations.AddField(
            model_name='post',
            name='shared_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='shared_body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='shared_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
