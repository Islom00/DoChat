from django.urls import path

from accounts.views import IndexTemplateView, SignUpView

urlpatterns = [
    path("login", IndexTemplateView.as_view(), name="login"),
    path("signup", SignUpView.as_view(), name="signup"),
]
