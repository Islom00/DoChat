from django.db import models


class CustomUserModel(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    password_confirmation = models.CharField(max_length=50)
