from django.forms import ModelForm, Select, Textarea, TextInput

from .models import Comment, Post, Subscriber


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "content", "author_id"]
        widgets = {
            "title": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Title",
            }),
            "description": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Short description",
            }),
            "content": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Input text",
            }),
            "author_id": Select(attrs={
                "required": "required",
                "class": "form-control",
            }),
        }


class SubscribeForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email_to", "author_id"]
        widgets = {
            "email_to": TextInput(attrs={
                "required": "required",
                "class": "form-control",
                "placeholder": "Your email",
                # "pattern": "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$"
                # Валидация через HTML. Пишут не надежная...? Пока оставлю серверную валидацию мыла, эту закомменчу.
            }),
            "author_id": Select(attrs={
                "required": "required",
                "class": "form-control",
                "placeholder": "Your email",
            }),
        }

    def __init__(self, *args, **kwargs):
        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.fields['author_id'].empty_label = None
        self.fields['author_id'].initial = 1


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": Textarea(attrs={
                "class": "form-control",
                "placeholder": "Input text",
                "rows": 3,
            }),
        }
