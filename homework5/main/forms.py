from django.forms import ModelForm, TextInput

from .models import Post


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
