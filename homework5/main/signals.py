from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Author


@receiver(pre_save, sender=Author)
def author_pre_save(sender, instance, *args, **kwargs):
    print("pre-save-------------")
    instance.name = "Karl"


@receiver(post_save, sender=Author)
def author_post_save(sender, instance, created, *args, **kwargs):
    print("post-save-------------")
    if created:
        print('Author created')
    else:
        print('Author exist')
