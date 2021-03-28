from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url


ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


def about(request, *args, **kwargs):
    return render(request, "pages/about.html", context={}, status=200)