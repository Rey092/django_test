from django.core.mail import send_mail


def email_send(email_to, author_name):
    send_mail(
        'Bread Blog',
        f'You have subscribed on Author: {author_name}',
        'worker.omega@gmail.com',
        [email_to],
        fail_silently=False,
    )


def telegram_send(email_to):
    # TODO: telegram_send()
    pass


def send_email_with_custom_text(email_to, text):
    send_mail(
        'Bread Blog',
        f'{text}',
        'worker.omega@gmail.com',
        [email_to],
        fail_silently=False,
    )
