from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from product.models import ProductVariant
from campaign.models import Campaign

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="item")
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="cart_product"
    )
    campaign = models.ForeignKey(
        Campaign,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="cart_campaign",
    )
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "variant"], name="unique product in cart"
            )
        ]

    def __str__(self):
        return self.variant.sku

    def get_item_price(self):
        price = self.variant.price
        discount = self.campaign.discount if self.campaign else Decimal(0.00)
        return price - (discount / 100) * price
