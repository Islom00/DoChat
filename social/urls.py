from django.urls import path

from social.views import PostListView, PostDetailView, PostEditView, PostDeleteView, CommentDeleteView, ProfileView, \
    ProfileEditView, AddFollower, RemoveFollower, PostAddView, AddLike, AddDislike, UserSearchListView, \
    UserFollowersListView

app_name = "social"

urlpatterns = [
    path("", PostListView.as_view(), name="posts"),
    path("post/add", PostAddView.as_view(), name="add-post"),
    path("post/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path("post/edit/<int:pk>", PostEditView.as_view(), name="post-edit"),
    path("post/delete/<int:pk>", PostDeleteView.as_view(), name="post-delete"),
    path("post/<int:post_pk>/comment/delete/<int:pk>", CommentDeleteView.as_view(), name="comment-delete"),
    path("post/<int:pk>/like", AddLike.as_view(), name="post-like"),
    path("post/<int:pk>/dislike", AddDislike.as_view(), name="post-dislike"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("profile/edit/<int:pk>", ProfileEditView.as_view(), name="profile-edit"),
    path("profile/<int:pk>/followers/add", AddFollower.as_view(), name="follower-add"),
    path("profile/<int:pk>/followers/remove", RemoveFollower.as_view(), name="follower-remove"),
    path("search/", UserSearchListView.as_view(), name="profile-search"),
    path("profile/<int:pk>/followers", UserFollowersListView.as_view(), name="user-followers"),
]

