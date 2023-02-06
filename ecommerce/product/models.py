from django.db import models
from django.core.validators import MinValueValidator
from category.models import Category
from decimal import Decimal


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    category = models.ManyToManyField(Category, related_name="products")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    name = models.CharField(max_length=32)
    value = models.CharField(max_length=32)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name + " | " + self.value


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variant"
    )
    attribute = models.ManyToManyField(
        ProductAttribute, related_name="product_variants"
    )
    sku = models.CharField(max_length=64)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price in USD",
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    currency = models.CharField(max_length=3, default="USD", choices=(("USD", "USD"),))
    image = models.ImageField(upload_to="productImage/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return self.sku
