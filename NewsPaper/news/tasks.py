from celery import shared_task
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


@shared_task
def test():
    print('Test')


@shared_task
def send_notifications_category(emails, preview, pk, title):
    print('start send email in task')
    for email in emails:
        send_notifications(preview, pk, title, [email, ])
    print('end send email in task')


def send_notifications(preview, pk, title, subscribers):
    print(subscribers)

    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{ settings.SITE_URL }/news/post/{ pk }'
        }
    )

    msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subscribers
        )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()