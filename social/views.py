from django.shortcuts import render
from django.views import View

from social.forms import PostForm
from social.models import Post


class PostListView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by("-created_at")
        form = PostForm()

        context = {
            "posts": posts,
            "form": form,
        }
        return render(request, "social/social.html", context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by("-created_at")
        form = PostForm(request.POST)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            "posts": posts,
            "form": form,
        }
        return render(request, "social/social.html", context)
