from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from django.conf import settings
from .models import PostCategory

from .tasks import test, send_notifications_category

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


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    print('Start send email')
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        emails = list(categories.values_list('subcribers__email', flat=True))

        # test.delay()
        # Можно просто передать post.pk, но была рекомендация что бы в задачу передавались только данные.
        # Мне кажется это не совсем верным, ошибаюсь?
        send_notifications_category.delay(emails=emails, preview=instance.preview(), pk=instance.pk, title=instance.title)

        # Вынесено в задачу
        # for category in categories:
        #     for sub in category.subcribers.all():
        #         send_notifications(instance.preview(), instance.pk, instance.title, [sub.email, ])
        #         print('end send email')

