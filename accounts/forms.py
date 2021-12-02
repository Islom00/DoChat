from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUserModel


class SignUpForm(UserCreationForm):
    model = CustomUserModel
    fields = "__all__"
