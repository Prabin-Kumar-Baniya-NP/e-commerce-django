import os
from django.dispatch import receiver
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image of Product Variant when the object is deleted
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=User)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old image of Product Variant when it is updated with new image
    """
    if not instance.pk:
        return False

    try:
        old_image = User.objects.get(pk=instance.pk).image
    except User.DoesNotExist:
        return False

    if old_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
