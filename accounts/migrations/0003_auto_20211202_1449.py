# Generated by Django 3.2.9 on 2021-12-02 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customusercreation_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('password_confirmation', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='CustomUserCreation',
        ),
    ]