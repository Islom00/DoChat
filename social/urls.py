from django.urls import path

from social.views import PostListView, PostDetailView, PostEditView, PostDeleteView, CommentDeleteView, ProfileView, \
    ProfileEditView, AddFollower, RemoveFollower, PostAddView, UserSearch, \
    UserFollowersList, PostLike, PostDislike, CommentLike, CommentDislike, CommentReply, ListThreads, CreateThreadView, \
    ThreadView, CreateMessage, ThreadDeleteView

app_name = "social"

urlpatterns = [
    path("", PostListView.as_view(), name="posts"),
    path("post/add", PostAddView.as_view(), name="add-post"),
    path("post/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path("post/edit/<int:pk>", PostEditView.as_view(), name="post-edit"),
    path("post/delete/<int:pk>", PostDeleteView.as_view(), name="post-delete"),
    path("post/<int:post_pk>/comment/delete/<int:pk>", CommentDeleteView.as_view(), name="comment-delete"),
    path("post/<int:post_pk>/comment/like/<int:pk>", CommentLike.as_view(), name="comment-like"),
    path("post/<int:post_pk>/comment/dislike/<int:pk>", CommentDislike.as_view(), name="comment-dislike"),
    path("post/<int:post_pk>/comment/<int:pk>/reply", CommentReply.as_view(), name="comment-reply"),
    path("post/<int:pk>/like", PostLike.as_view(), name="post-like"),
    path("post/<int:pk>/dislike", PostDislike.as_view(), name="post-dislike"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path("profile/edit/<int:pk>", ProfileEditView.as_view(), name="profile-edit"),
    path("profile/<int:pk>/followers/add", AddFollower.as_view(), name="follower-add"),
    path("profile/<int:pk>/followers/remove", RemoveFollower.as_view(), name="follower-remove"),
    path("search/", UserSearch.as_view(), name="profile-search"),
    path("profile/<int:pk>/followers", UserFollowersList.as_view(), name="user-followers"),
    path("inbox/", ListThreads.as_view(), name="inbox"),
    path("inbox/create-thread", CreateThreadView.as_view(), name="create-thread"),
    path("inbox/<int:pk>/delete-thread", ThreadDeleteView.as_view(), name="thread-delete"),
    path("inbox/<int:pk>/", ThreadView.as_view(), name="thread"),
    path("inbox/<int:pk>/create-message", CreateMessage.as_view(), name="create-message"),
]


