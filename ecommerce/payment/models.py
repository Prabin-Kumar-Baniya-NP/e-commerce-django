from django.db import models
from order.models import Order

PROVIDER_PROVIDER = (
    ("Stripe", "Stripe"),
    ("PayPal", "PayPal"),
    ("Paytm", "Paytm"),
)

PAYMENT_CHOICES = (
    ("PS", "Payment Started"),
    ("PF", "Payment Failed"),
    ("PC", "Payment Completed"),
    ("PR", "Payment Refunded"),
)


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name="payment")
    provider = models.CharField(max_length=32, choices=PROVIDER_PROVIDER)
    status = models.CharField(max_length=2, choices=PAYMENT_CHOICES, default="PS")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + " | " + self.order.user.get_full_name()
