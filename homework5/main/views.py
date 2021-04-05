from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .forms import PostForm, SubscribeForm
from .services.notify_service import notify
from .services.post_service import posts_all, posts_by_author
from .services.subscribe_service import get_author, subscribe

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request):
    return render(request, "pages/home.html")


def about(request):
    return render(request, "pages/about.html")


def posts(request):
    return render(request, "pages/post.html", {"posts": posts_all()})


def author_posts(request, author_id):
    return render(request, "pages/post.html", {"posts": posts_by_author(author_id)})


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = PostForm()

    return render(request, "pages/post_create.html", context={'form': form})


def api_posts(request):
    data = [post.serialize() for post in posts_all()]
    return JsonResponse(data, safe=False)


def api_subscribe(request):
    email_to = request.GET["email_to"]
    author = get_author(request)

    subscribe(author, email_to)
    notify(email_to)

    return HttpResponse(f"You are subscribed on {author}")


def posts_subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()

            author = get_author(request)
            context = author.serialize()

            return render(request, "pages/subscribe_success.html", context=context)
    else:
        form = SubscribeForm()

    return render(request, "pages/subscribe.html", context={"form": form})
