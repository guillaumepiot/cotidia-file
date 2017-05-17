import uuid
import magic

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

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        storage = self.f.storage
        self.name = self.f.name
        self.mimetype = magic.from_buffer(self.f.read(), mime=True)
        super().save(*args, **kwargs)
