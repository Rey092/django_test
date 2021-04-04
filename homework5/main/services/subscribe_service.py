from django.core.exceptions import ObjectDoesNotExist
from main.models import Subscriber


subscribe_email_pattern = r"(?!(^[.-].*|[^@]*[.-]@|.*\.{2,}.*)|^.{254}.)([a-zA-Z0-9!#$%&'*+\/=?^_`{|}~.-]+@)(?!-.*|.*-\.)([a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,15}"


def subscribe(author_id, email_to):
    try:
        Subscriber.objects.get(email_to=email_to, author_id=author_id)
    except ObjectDoesNotExist:
        subscriber = Subscriber(email_to=email_to, author_id=author_id)
        subscriber.save()
