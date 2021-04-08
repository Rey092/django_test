from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from faker import Faker

from .forms import PostForm, SubscribeForm
from .models import Author, Post
from .services.authors_service import get_all_authors
from .services.notify_service import notify
from .services.post_service import post_find, posts_all, posts_by_author
from .services.subscribe_service import get_all_subscribers, get_author, subscribe

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request):
    return render(request, "pages/home.html")


def about(request):
    return render(request, "pages/about.html")


def posts(request):
    return render(request, "pages/posts_all.html", {"posts": posts_all()})


def author_posts(request, author_id):
    return render(request, "pages/posts_all.html", {"posts": posts_by_author(author_id)})


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = PostForm()

    return render(request, "pages/post_create.html", context={'form': form})


def post_show(request, post_id):
    post = post_find(post_id)
    return render(request, 'pages/post_show.html', context={"post": post})


def post_update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    err = ""
    if request.method == "POST":
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts_all")
        else:
            err = "error on update post"
    else:
        form = PostForm(instance=post)
    context = {
        "form": form,
        "err": err,
    }
    return render(request, "pages/post_edit.html", context=context)


def subscribers_new(request):
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


def subscribers_all(request):
    return render(request, "pages/subscribers.html", {"subscribers": get_all_subscribers()})


def authors_all(request):
    return render(request, "pages/authors.html", {"authors": get_all_authors()})


def authors_new(request):
    faker = Faker()
    Author(name=faker.name(), email=faker.email()).save()
    return redirect("authors_all")


def api_posts(request):
    data = [post.serialize() for post in posts_all()]
    return JsonResponse(data, safe=False)


def api_subscribe(request):
    email_to = request.GET["email_to"]
    author = get_author(request)

    subscribe(author, email_to)
    notify(email_to)

    return HttpResponse(f"You are subscribed on {author}")


def api_authors_new(request):
    faker = Faker()
    Author(name=faker.name(), email=faker.email()).save()
    authors = Author.objects.all().values("name", "email")
    return JsonResponse(list(authors), safe=False)
