from celery import shared_task
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category
import datetime

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


@shared_task
def periodic_mailing():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(create_date_time__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    emails = set(Category.objects.filter(name__in=categories).values_list('subcribers__email', flat=True))

    for email in emails:
        if email:
            send_daily_posts(posts, [email, ])
            print('end send email')


def send_daily_posts(posts, subscribers):
    print(subscribers)

    html_context = render_to_string(
        'daily_posts.html',
        {
            'posts': posts,
            'link': settings.SITE_URL
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()