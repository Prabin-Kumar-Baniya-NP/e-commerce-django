from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from product.models import Product


class Campaign(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    product = models.ManyToManyField(Product, related_name="product_promotion")
    discount = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    promocode = models.CharField(max_length=16)
    auto_apply = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.promocode
