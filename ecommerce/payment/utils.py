from django.contrib.auth import get_user_model
from notification.tasks import notify_by_email

User = get_user_model()


def send_order_confirmation_email(user_id, order_id):
    subject = "Your order is successfully placed"
    message = f"Your recent order having id {order_id} is successfully placed."
    recipient = User.objects.get(id=user_id).email
    notify_by_email.delay(subject, message, recipient)


def send_payment_succeeded_email(user_id, payment_id, amount, currency):
    subject = "Payment Confirmation"
    message = (
        f"The payment of {amount} {currency} was completed. Paymend ID is {payment_id}."
    )
    recipient = User.objects.get(id=user_id).email
    notify_by_email.delay(subject, message, recipient)


def send_payment_failed_email(user_id, amount, currency, error_message):
    subject = "Your last payment was failed"
    message = (
        f"The payment of {amount} {currency} was failed because {error_message.lower()}"
    )
    recipient = User.objects.get(id=user_id).email
    notify_by_email.delay(subject, message, recipient)
