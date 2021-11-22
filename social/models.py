from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.ImageField(upload_to="media/posts", null=True, blank=True)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True,
        verbose_name="user",
        related_name="profile",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=30, blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(
        upload_to="media/profile_pictures",
        default="media/profile_pictures/default.png",
        blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name="followers")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()







