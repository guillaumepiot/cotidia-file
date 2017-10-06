from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from cotidia.file.models import File
from cotidia.file.conf import settings
from cotidia.file.utils.variation import generate_variation


@receiver(pre_save, sender=File)
def set_order_id(sender, instance, **kwargs):
    if not instance.order_id:
        # Set initial order id
        last_file = File.objects.filter(
            content_type=instance.content_type,
            object_id=instance.object_id
        ).exclude(order_id=None).last()
        if last_file:
            instance.order_id = last_file.order_id + 1
        else:
            instance.order_id = 1


@receiver(post_save, sender=File)
def handle_image_variations(sender, instance, created, **kwargs):
    if created:
        if instance.is_raster_image and settings.FILE_IMAGE_VARIATIONS:
            for variation in settings.FILE_IMAGE_VARIATIONS.keys():
                generate_variation(instance, variation)
