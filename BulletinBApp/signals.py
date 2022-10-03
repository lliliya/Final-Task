from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Reply
from django.core.mail import EmailMultiAlternatives
# from BulletinBoard.settings import DEFAULT_FROM_EMAIL


@receiver(post_save, sender=Reply)
def notify_user_reply(sender, instance, created, **kwargs):
    email = instance.ad.user.email
    html_content = render_to_string('account/notify_reply.html', {'reply': instance})
    msg = EmailMultiAlternatives(
        subject=f'{instance.user.username} откликнулся на ваше объявление',
        from_email=DEFAULT_FROM_EMAIL,
        to=[email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
