import io
from time import time

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.list import ListView
from faker import Faker
from xlsxwriter.workbook import Workbook

from .forms import CommentForm, PostForm, SubscribeForm
from .models import Author, Book, Category, Comment, ContactUs, Post
from .services.authors_service import get_all_authors
from .services.post_service import get_all_posts, get_comments_for_post, get_post, posts_by_author
from .services.subscribe_service import get_all_subscribers, get_author, subscribe
from .tasks import notify_async, send_email_to_all_subscribers

# -----------------------------------------------------------
# view functions for posts - models: Post, Author
# -----------------------------------------------------------


class PostsListView(ListView):
    template_name = 'pages/post_list.html'

    def get_queryset(self):
        posts_list_qs = cache.get('posts_list_qs')
        if not posts_list_qs:
            posts_list_qs = get_all_posts()
            cache.set('posts_list_qs', posts_list_qs)
        return posts_list_qs


def author_posts(request, author_id):
    return render(request, "pages/post_list.html", {"post_list": posts_by_author(author_id)})


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("post_list")
    else:
        form = PostForm()

    return render(request, "pages/post_create.html", context={'form': form})


def post_show(request, post_id):
    post = get_post(post_id)
    comments = get_comments_for_post(post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        Comment(content=form.cleaned_data['content'], post_id=post).save()
        return redirect("post_show", post_id)
    else:
        form = CommentForm()
    context = {
        "post": post,
        "form": form,
        "comments": comments
    }
    return render(request, 'pages/post_show.html', context=context)


def post_update(request, post_id):
    post = get_post(post_id)
    err = ""
    authenticated = False

    if request.user.is_authenticated:
        if request.user.id == post.author_id.id:
            authenticated = True

    if request.method == "POST":
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid() and authenticated:
            if request.POST.get('delete'):
                form.instance.delete()
            else:
                form.save()
            return redirect("post_list")
        else:
            err = "error on update or delete post"
    else:
        form = PostForm(instance=post)

    context = {
        "form": form,
        "err": err,
        "authenticated": authenticated
    }
    return render(request, "pages/post_edit.html", context=context)


# -----------------------------------------------------------
# view functions for authors - models: Author, Subscriber
# -----------------------------------------------------------


def authors_new(request):
    # manager = UserProfileManager()
    faker = Faker()

    # Author(name=faker.name(), email=faker.email(), password='qwerty').save()
    Author.objects.create_user(email=faker.email(), name=faker.name(), password='qwerty')

    return redirect("author_list")


class AuthorsListView(ListView):
    template_name = 'pages/author_list.html'

    def get_queryset(self):
        authors_list_qs = cache.get('authors_list_qs')
        if not authors_list_qs:
            authors_list_qs = Author.objects.all().prefetch_related("books")
            cache.set('authors_list_qs', authors_list_qs)
        return authors_list_qs

    def get_context_data(self, **kwargs):
        context = super(AuthorsListView, self).get_context_data(**kwargs)
        authenticated = True if self.request.user.is_authenticated else False
        context['authenticated'] = authenticated
        return context


# def authors_all(request):
#     authenticated = False
#
#     if request.user.is_authenticated:
#         author = Author.objects.filter(id=request.user.id)[0]
#         if request.user.id == author.id:
#             authenticated = True
#         if authenticated and request.POST.get('delete'):
#             author.delete()
#             return redirect("post_list")
#
#     authors_qs = cache.get('authors_list_qs')
#     if not authors_qs:
#         authors_qs = Author.objects.all().prefetch_related("books")
#         cache.set('authors_list_qs', authors_qs)
#
#     context = {
#         "authors_qs": authors_qs,
#         "authenticated": authenticated
#     }
#     return render(request, "pages/author_list.html", context=context)


def remove_obj(request, pk):
    obj = get_object_or_404(Author, id=pk)

    if request.user.id == obj.id:
        obj.delete()

    return redirect("author_list")


def author_subscribe(request):
    form = SubscribeForm(request.POST or None)
    # , initial = {'author_id': 1}

    if form.is_valid():
        form.save()

        author = get_author(request)
        email_to = request.POST.get('email_to')

        notify_async.delay(email_to, author.name)
        # notify_async.apply_async(args=(email_to, author.name), countdown=5)

        context = author.serialize()
        return render(request, "pages/subscribe_success.html", context=context)

    return render(request, "pages/subscribe.html", context={"form": form})


def author_subscribers_all(request):
    return render(request, "pages/subscribers.html", {"subscribers": get_all_subscribers()})


# -----------------------------------------------------------
# view functions for Books and Categories - models: Book, Category
# -----------------------------------------------------------


def books_all(request):
    context = {
        "books": Book.objects.all().only("title", "category_id__title").select_related("category_id")
    }
    return render(request, "pages/books.html", context=context)


class CategoriesListView(ListView):
    template_name = 'pages/categories.html'

    def get_queryset(self):
        categories_list_qs = cache.get('categories_list_qs')
        if not categories_list_qs:
            categories_list_qs = Category.objects.all().prefetch_related("books")
            cache.set('categories_list_qs', categories_list_qs)
        return categories_list_qs
# -----------------------------------------------------------
# view functions for API - models: Author, Subscriber, Post
# -----------------------------------------------------------


def json_posts(request):
    data = [post.serialize() for post in get_all_posts()]
    return JsonResponse(data, safe=False)


def api_post_show(request, post_id=1):
    data = get_post(post_id).serialize()
    return JsonResponse(data, safe=False)


def api_subscribe(request):
    email_to = request.GET["email_to"]
    author = get_author(request)

    subscribe(author, email_to)
    notify_async(email_to, author.name)

    return HttpResponse(f"You are subscribed on {author}")


def api_subscribers_all(request):
    data = [subscriber.serialize() for subscriber in get_all_subscribers()]
    return JsonResponse(data, safe=False)


def api_authors_all(request):
    data = [author.serialize() for author in get_all_authors()]
    return JsonResponse(data, safe=False)


def api_authors_new(request):
    faker = Faker()
    Author(name=faker.name(), email=faker.email()).save()
    authors = Author.objects.all().values("name", "email")
    return JsonResponse(list(authors), safe=False)


def test(request):
    st = time()
    print('----start')
    send_email_to_all_subscribers.delay()
    time_exec = time() - st
    print(f'----finish. time_exec: {time_exec}')
    return redirect('about_page')


class CreateContactUsView(CreateView):
    success_url = reverse_lazy('home_page')
    model = ContactUs
    template_name = 'pages/contactus_form.html'
    fields = ('email', 'subject', 'message')


def medusweet_xlsx(request):
    output = io.BytesIO()

    workbook = Workbook(output, {'in_memory': True})

    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 100)
    worksheet.write(0, 0, 'Title')
    worksheet.write(0, 1, 'Content')
    worksheet.set_default_row(70)

    cell_format = workbook.add_format()
    cell_format.set_text_wrap()

    queryset = Post.objects.values('title', 'content')
    row = 1
    for obj in queryset.iterator():
        worksheet.write(row, 0, obj['title'], cell_format)
        worksheet.write(row, 1, obj['content'], cell_format)
        row += 1

    workbook.close()
    output.seek(0)

    response = HttpResponse(output.read(), content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = "attachment; filename=medusweet_data.xlsx"

    output.close()

    return response
