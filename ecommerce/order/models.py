from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

ORDER_STATUS = (
    ("PP", "Payment Pending"),
    ("PF", "Payment Fulfilled"),
    ("OP", "Order Placed"),
    ("AP", "Order Approved"),
    ("RJ", "Order Rejected"),
    ("SH", "Order Shipped"),
    ("OD", "Order Delivered"),
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="order")
    status = models.CharField(max_length=2, choices=ORDER_STATUS, default="PP")
    shipping_address = models.JSONField()
    order_items = models.JSONField()
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    currency = models.CharField(max_length=3, default="USD", choices=(("USD", "USD"),))
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() + " | " + str(self.id)
