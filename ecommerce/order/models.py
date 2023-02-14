from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from user.models import Address
from product.models import ProductVariant
from campaign.models import Campaign

User = get_user_model()

ORDER_STATUS = (
    ("CREATED", "ORDER CREATED"),
    ("PLACED", "ORDER PLACED"),
    ("APPROVED", "ORDER APPROVED"),
    ("REJECTED", "ORDER REJECTED"),
    ("SHIPPED", "ORDER SHIPPED"),
    ("DELIVERED", "ORDER DELIVERED"),
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="order")
    status = models.CharField(max_length=32, choices=ORDER_STATUS, default="PP")
    shipping_address = models.ForeignKey(
        Address, on_delete=models.RESTRICT, related_name="order_address"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    currency = models.CharField(max_length=3, default="USD", choices=(("USD", "USD"),))
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_item"
    )
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.RESTRICT, related_name="order_item"
    )
    campaign = models.ForeignKey(
        Campaign, on_delete=models.RESTRICT, related_name="order_item", null=True, blank=True
    )
    quantity = models.PositiveIntegerField()
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD", choices=(("USD", "USD"),))
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
