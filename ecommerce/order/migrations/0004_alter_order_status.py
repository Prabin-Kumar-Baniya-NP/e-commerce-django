# Generated by Django 4.1.5 on 2023-01-24 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0003_alter_orderitem_campaign"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("PP", "Payment Pending"),
                    ("PF", "Payment Fulfilled"),
                    ("OP", "Order Placed"),
                    ("AP", "Order Approved"),
                    ("RJ", "Order Rejected"),
                    ("SH", "Order Shipped"),
                    ("OD", "Order Delivered"),
                ],
                default="PP",
                max_length=2,
            ),
        ),
    ]
