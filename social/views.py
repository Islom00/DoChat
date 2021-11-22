from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView

from social.forms import PostForm, CommentForm
from social.models import Post, Comment, UserProfile


class PostListView(LoginRequiredMixin, View):
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


class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by("-created_at")

        context = {
            "post": post,
            "form": form,
            "comments": comments,
        }

        return render(request, "social/post_detail.html", context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)
        comments = Comment.objects.filter(post=post).order_by("-created_at")

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

        context = {
            "post": post,
            "form": form,
            "comments": comments,
        }

        return render(request, "social/post_detail.html", context)


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["body"]
    template_name = "social/post_edit.html"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("social:post-detail", kwargs={"pk": pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "social/post_delete.html"
    success_url = reverse_lazy("social:posts")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "social/comment_delete.html"

    def get_success_url(self):
        pk = self.kwargs["post_pk"]
        return reverse_lazy("social:post-detail", kwargs={"pk": pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by("-created_at")
        followers = profile.followers.all()

        if len(followers) == 0:
            is_following = False

        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False

        number_of_followers = len(followers)

        context = {
            "profile": profile,
            "user": user,
            "posts": posts,
            "num_of_followers": number_of_followers,
            "is_following": is_following,
        }
        return render(request, "social/profile.html", context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ["avatar", "name", "birth_date", "bio"]
    template_name = "social/profile_edit.html"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("social:profile", kwargs={"pk": pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user


class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        return redirect("social:profile", pk=profile.pk)


class RemoveFollower(View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect("social:profile", pk=profile.pk)


