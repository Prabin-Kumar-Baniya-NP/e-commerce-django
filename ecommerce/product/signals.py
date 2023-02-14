import os
from django.dispatch import receiver
from django.db import models
from product.models import ProductVariant


@receiver(models.signals.post_delete, sender=ProductVariant)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image of Product Variant when the object is deleted
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=ProductVariant)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old image of Product Variant when it is updated with new image
    """
    if not instance.pk:
        return False

    try:
        old_image = ProductVariant.objects.get(pk=instance.pk).image
    except ProductVariant.DoesNotExist:
        return False

    if old_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
