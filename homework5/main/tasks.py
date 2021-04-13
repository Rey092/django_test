from datetime import timedelta

from bs4 import BeautifulSoup
from celery import shared_task
from django.utils.timezone import now
import requests

from .models import Logger, Subscriber
from .services.notify_service import email_send, send_email_with_custom_text


@shared_task
def notify_async(email_to, author_name):
    email_send(email_to, author_name)


@shared_task
def delete_logs_async():
    how_many_days = 3
    Logger.objects.filter(created__lte=now() - timedelta(days=how_many_days)).delete()


@shared_task
def send_email_to_all_subscribers():
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/51.0'
    }
    url = requests.get("https://tproger.ru/wp-content/plugins/citation-widget/get-quote.php", headers)
    text = BeautifulSoup(url.content, 'html.parser')
    emails = Subscriber.objects.values_list('email_to', flat=True)

    for email in set(emails):
        send_email_with_custom_text(email, text)
