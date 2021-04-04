from django.forms import ModelForm, TextInput, Select

from .models import Post, Subscriber
from .services.subscribe_service import subscribe_email_pattern


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "content"]
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
        }


BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']


class SubscribeForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email_to", "author_id"]

        widgets = {
            "email_to": TextInput(attrs={
                "required": "required",
                "class": "form-control",
                "placeholder": "Your email",
                # "pattern": subscribe_email_pattern -
                # валидация через HTML пишут не надежная. Пока оставлю ток серверную валидацию мыла, эту закомменчу.
            }),
            "author_id": Select(attrs={
                "required": "required",
                "class": "form-control",
                "initial": 0  # TODO: Понять что написать. В принципе и так работает
            }),
        }
