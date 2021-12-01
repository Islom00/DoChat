from django.contrib import admin

from social.models import Post, Comment, UserProfile, MessageModel, ThreadModel

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(MessageModel)
admin.site.register(ThreadModel)
