from django.dispatch import receiver
from django.db.models.signals import post_save

from cotidia.file.models import File
from cotidia.file.conf import settings
from cotidia.file.utils.variation import generate_variation


@receiver(post_save, sender=File)
def handle_image_variations(sender, instance, created, **kwargs):
    if created:
        if instance.is_raster_image and settings.FILE_IMAGE_VARIATIONS:
            for variation in settings.FILE_IMAGE_VARIATIONS.keys():
                generate_variation(instance, variation)
