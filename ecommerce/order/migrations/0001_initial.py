# Generated by Django 4.1.5 on 2023-02-14 08:55

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("product", "0001_initial"),
        ("campaign", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("CREATED", "ORDER CREATED"),
                            ("PLACED", "ORDER PLACED"),
                            ("APPROVED", "ORDER APPROVED"),
                            ("REJECTED", "ORDER REJECTED"),
                            ("SHIPPED", "ORDER SHIPPED"),
                            ("DELIVERED", "ORDER DELIVERED"),
                        ],
                        default="PP",
                        max_length=32,
                    ),
                ),
                (
                    "total_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.00"))
                        ],
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        choices=[("USD", "USD")], default="USD", max_length=3
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="OrderItemSerializer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("initial_price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "discount_percent",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("final_price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "currency",
                    models.CharField(
                        choices=[("USD", "USD")], default="USD", max_length=3
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "campaign",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="order_item",
                        to="campaign.campaign",
                    ),
                ),
                (
                    "variant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="order_item",
                        to="product.productvariant",
                    ),
                ),
            ],
        ),
    ]
