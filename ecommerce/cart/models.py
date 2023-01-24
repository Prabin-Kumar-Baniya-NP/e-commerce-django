from django.db import models
from django.contrib.auth import get_user_model
from product.models import Variation
from campaign.models import Campaign

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_cart")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(
        Variation, on_delete=models.CASCADE, related_name="cart_product"
    )
    campaign = models.ForeignKey(
        Campaign,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="campaign",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return self.product.name
