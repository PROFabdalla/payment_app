from core import settings
from celery import shared_task
from django.core.mail import send_mail


@shared_task(bind=True)
def payment_succeed_mail(self, email):
    mail_subject = "hi! payment success"
    message = "don't do any action we just tell you"
    to_email = email
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )
    return "Send"
