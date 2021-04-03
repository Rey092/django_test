from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import PostForm
from .models import Post

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request):
    return render(request, "pages/home.html")


def about(request):
    return render(request, "pages/about.html")


def post(request):
    user_posts = Post.objects.all()
    return render(request, "pages/post.html", {"title": "Posts", "posts": user_posts})


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, "pages/post_create.html", context=context)


def post_api(request):
    data = [post.serialize() for post in Post.objects.all()]
    return JsonResponse(data, safe=False)
