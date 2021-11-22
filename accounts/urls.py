from django.urls import path

from accounts.views import IndexTemplateView, SignUpView

urlpatterns = [
    path("signup", SignUpView.as_view(), name="signup"),
]
