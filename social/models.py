from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.FileField(upload_to="media/posts", null=True, blank=True)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    dislikes = models.ManyToManyField(User, blank=True, related_name="dislikes")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name="comment_likes")
    dislikes = models.ManyToManyField(User, blank=True, related_name="comment_dislikes")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="+")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by("-created_at").all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


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

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ThreadModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")


class MessageModel(models.Model):
    thread = models.ForeignKey("ThreadModel", related_name="+", on_delete=models.CASCADE, blank=True, null=True)
    send_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to="message_photos", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)





