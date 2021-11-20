from django.urls import path

from social.views import PostListView

app_name = "social"

urlpatterns = [
    path("", PostListView.as_view(), name="posts")
]