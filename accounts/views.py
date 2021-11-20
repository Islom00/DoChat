from django.shortcuts import render
from django.views.generic import TemplateView


class IndexTemplateView(TemplateView):
    template_name = "registration/login.html"


class SignUpView(TemplateView):
    template_name = "registration/signup.html"

