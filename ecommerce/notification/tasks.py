from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings
from twilio.rest import Client


@shared_task()
def notify_by_email(subject, message, recipient):
    send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])


@shared_task()
def notify_by_sms(message, phone_number):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number,
    )
