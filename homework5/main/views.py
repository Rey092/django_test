from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from .forms import PostForm, SubscribeForm
from .models import Author
from .services.notify_service import notify
from .services.post_service import posts_all
from .services.subscribe_service import subscribe

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request):
    return render(request, "pages/home.html")


def about(request):
    return render(request, "pages/about.html")


def posts(request):
    return render(request, "pages/post.html", {"title": "Posts", "posts": posts_all()})


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


def api_posts(request):
    data = [post.serialize() for post in posts_all()]
    return JsonResponse(data, safe=False)


def api_subscribe(request):
    author_id = request.GET["author_id"]
    email_to = request.GET["email_to"]

    author = get_object_or_404(Author, pk=author_id)

    subscribe(author, email_to)
    notify(email_to)

    data = {"author_id": author_id}
    return HttpResponse(f"You are subscribed on {author}")


def posts_subscribe(request):
    err_email, err_subscribe = "d-none", "d-none"
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            err_email = ""
    else:
        form = SubscribeForm()
    context = {
        "form": form,
        "err_email": err_email,
        "err_subscribe": err_subscribe,
    }
    return render(request, "pages/subscribe.html", context=context)
