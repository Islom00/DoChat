from django import forms

from social.models import Post, Comment


class PostForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": "3",

            }
        )
    )
    content = forms.ImageField(required=False)

    class Meta:
        model = Post
        exclude = ["created_at", "author", "likes", "dislikes"]


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": "3",
                "placeholder": "Comment on this post !"
            }
        )
    )

    class Meta:
        model = Comment
        fields = ["comment"]


class ThreadForm(forms.Form):
    username = forms.CharField(label="", max_length=100)


class MessageForm(forms.Form):
    message = forms.CharField(label="", max_length=1000)