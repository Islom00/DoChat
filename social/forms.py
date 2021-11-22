from django import forms

from social.models import Post, Comment


class PostForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": "3",
                "placeholder": "Say something ..."
            }
        )
    )

    class Meta:
        model = Post
        exclude = ["created_at", "author"]


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": "3",
                "placeholder": "Say something ..."
            }
        )
    )

    class Meta:
        model = Comment
        fields = ["comment"]
