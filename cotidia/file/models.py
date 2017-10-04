import uuid
import magic

from django.core.files.images import get_image_dimensions

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from cotidia.file.conf import settings


class File(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    f = models.FileField(upload_to=settings.FILE_UPLOAD_PATH)
    name = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=255)

    # Generic relation
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # File related data
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    size = models.IntegerField(null=True)

    taxonomy = models.CharField(max_length=255, null=True)

    order_id = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
        ordering = ("order_id", "-created_at",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.f.name
        self.mimetype = magic.from_buffer(self.f.read(), mime=True)
        self.size = self.f.size
        if self.is_image:
            self.width, self.height = get_image_dimensions(self.f)
        super().save(*args, **kwargs)

    @property
    def is_image(self):
        return self.mimetype.startswith("image")

    @property
    def is_raster_image(self):
        return self.mimetype in settings.FILE_RASTER_IMAGE_FORMATS

    def build_variation_path(self, variation):
        path_parts = self.f.name.split("/")
        path_parts.insert(-1, variation)
        return "/".join(path_parts)
