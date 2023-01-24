from django.db import models
from django.core.validators import MinValueValidator
from category.models import Category
from decimal import Decimal


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    category = models.ManyToManyField(Category, related_name="category")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Variation(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variation"
    )
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=64)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price in USD",
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    image = models.ImageField(upload_to="productImage/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
