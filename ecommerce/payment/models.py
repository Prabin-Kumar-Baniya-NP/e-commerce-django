from django.db import models
from order.models import Order

PROVIDER_PROVIDER = (("STRIPE", "STRIPE"),)

PAYMENT_CHOICES = (
    ("REQUESTED", "REQUESTED"),
    ("FAILED", "FAILED"),
    ("COMPLETED", "COMPLETED"),
)


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name="payment")
    provider = models.CharField(max_length=32, choices=PROVIDER_PROVIDER)
    status = models.CharField(max_length=32, choices=PAYMENT_CHOICES, default="REQUESTED")
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
