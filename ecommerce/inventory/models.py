from django.db import models
from product.models import ProductVariant


class Inventory(models.Model):
    product_varient = models.OneToOneField(
        ProductVariant,
        on_delete=models.CASCADE,
        verbose_name="Product Varient",
        related_name="product_inventory",
    )
    available = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventories"

    def __str__(self):
        return self.product_varient.name + " | " + self.product_varient.product.name
