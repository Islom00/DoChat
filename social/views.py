from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import UpdateView, DeleteView

from social.forms import PostForm, CommentForm
from social.models import Post, Comment, UserProfile


class PostAddView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        context = {
            "form": form,
        }
        return render(request, "social/add_post.html", context)

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            "form": form,
        }
        return render(request, "social/add_post.html", context)


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        ).order_by("-created_at")

        context = {
            "posts": posts,
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
    fields = ["title", "content", "body"]
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

        is_following = False

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
    fields = ["avatar", "name", "birth_date", "bio", "location"]
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


class PostLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)

        if is_like:
            post.likes.remove(request.user)

        next_url = request.POST.get('next', '/')
        return HttpResponseRedirect(next_url)


class PostDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next_url = request.POST.get('next', '/')
        return HttpResponseRedirect(next_url)


class UserSearch(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("query")
        profile_list = UserProfile.objects.filter(Q(
            user__username__icontains=query
        ))
        context = {
            "profile_list": profile_list
        }

        return render(request, "social/user_found.html", context)


class UserFollowersList(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile_followers = profile.followers.all()

        context = {
            "profile": profile,
            "profile_followers": profile_followers,
        }

        return render(request, "social/view_followers.html", context)


class CommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)

        if is_like:
            comment.likes.remove(request.user)

        next_url = request.POST.get('next', '/')
        return HttpResponseRedirect(next_url)


class CommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next_url = request.POST.get('next', '/')

        return HttpResponseRedirect(next_url)


class CommentReply(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        return redirect("social:post-detail", pk=post_pk)
