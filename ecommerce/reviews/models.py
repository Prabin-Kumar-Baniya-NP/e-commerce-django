from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Count, Avg

User = get_user_model()


class Reviews(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_reviews",
        verbose_name="Customer",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_reviews",
        verbose_name="Product",
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comment = models.TextField(max_length=1024)
    image = models.ImageField(upload_to="reviewsImage/", null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "product"]
        verbose_name = "Reviews"
        verbose_name_plural = "Reviews"
        ordering = ["created_at"]

    def __str__(self):
        return self.product.name + " | " + self.user.get_full_name()
