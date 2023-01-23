from django.db import models
from category.models import Category


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    category = models.ManyToManyField(Category, related_name="category")
    sku = models.CharField(max_length=64)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Price in USD"
    )
    image = models.ImageField(upload_to="productImage/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
