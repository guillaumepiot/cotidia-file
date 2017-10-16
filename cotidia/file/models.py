import uuid
import magic

from django.db import models
from django.utils.module_loading import import_string
from django.core.files.images import get_image_dimensions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from cotidia.file.conf import settings
from cotidia.admin.mixins import OrderableMixin
from cotidia.file.fields import CustomFileField


class File(models.Model, OrderableMixin):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    f = CustomFileField(upload_to=settings.FILE_UPLOAD_PATH)
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
    public = models.BooleanField(default=False)

    order_id = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
        ordering = ("order_id", "-created_at",)
        index_together = [
            ["content_type", "object_id", "order_id"],
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # @@TODO: move to signal
        if not self.id:
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

    def orderable_queryset(self):
        return self.__class__.objects.filter(
            content_type=self.content_type,
            object_id=self.object_id
        )

    @property
    def own_content_type(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return content_type

    def get_storage_class(self):
        if self.public:
            return settings.PUBLIC_FILE_STORAGE
        else:
            return settings.DEFAULT_FILE_STORAGE

    def get_storage(self):
        return import_string(self.get_storage_class())()
