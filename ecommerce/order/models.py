from django.db import models
from django.contrib.auth import get_user_model
from product.models import ProductVariant
from campaign.models import Campaign

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
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() + " | " + str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name="order")
    product = models.ForeignKey(
        ProductVariant, on_delete=models.RESTRICT, related_name="order_item"
    )
    quantity = models.PositiveIntegerField()
    campaign = models.ForeignKey(
        Campaign,
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        related_name="order_discount",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name
