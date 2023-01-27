# Generated by Django 4.1.5 on 2023-01-27 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("reviews", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="reviews",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_reviews",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Customer",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="reviews",
            unique_together={("user", "product")},
        ),
    ]
