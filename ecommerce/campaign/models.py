from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from product.models import Product
from decimal import Decimal


class Campaign(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024)
    product = models.ManyToManyField(Product, related_name="campaign")
    discount = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text="Value in percentage",
        validators=[MinValueValidator(Decimal("0.00"))],
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

    def is_valid_for_now(self):
        """
        Returns true if the campaign is valid for current datetime
        """
        now = timezone.now()
        if self.start_datetime <= now and self.end_datetime >= now:
            return True
        return False
