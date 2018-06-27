import magic

from django.template.defaultfilters import filesizeformat
from django.core.files.storage import default_storage

from rest_framework import serializers

from cotidia.file.models import File
from cotidia.file.conf import settings


class FileSerializer(serializers.ModelSerializer):

    f = serializers.FileField()

    class Meta:
        model = File
        fields = [
            'uuid',
            'f',
            'name',
            'mimetype',
            'size',
            'width',
            'height',
            'content_type',
            'object_id',
            'taxonomy',
            'created_at',
            'modified_at',
            'public'
        ]
        read_only_fields = [
            'uuid',
            'name',
            'mimetype',
            'size',
            'width',
            'height',
            'created_at',
            'modified_at',
        ]

    def validate_f(self, value):
        # Validate file type
        if len(settings.FILE_ALLOWED_TYPES) > 0:
            mimetype = magic.from_buffer(value.read(), mime=True)
            if mimetype not in settings.FILE_ALLOWED_TYPES:
                raise serializers.ValidationError(
                    'File type (%s) is invalid.' % mimetype
                )
            value.seek(0)
        # Validate file size
        if value.size > settings.FILE_MAX_UPLOAD_SIZE:
            raise serializers.ValidationError(
                "File size too large. It must be less than {}".format(
                    filesizeformat(settings.FILE_MAX_UPLOAD_SIZE))
            )

        return value

    def save(self, **kwargs):
        instance = super().save(**kwargs)

        storage = instance.get_storage_class()

        if storage.split(".")[-1] == "S3Boto3Storage":

            bucket = default_storage.bucket

            kwargs = {
                "Body": instance.f,
                "Key": instance.f.name,
            }

            if instance.mimetype == "image/svg+xml":
                kwargs["ContentType"] = instance.mimetype
                bucket.put_object(**kwargs)

        return instance


class FileOrderSerializer(serializers.Serializer):
    data = serializers.ListField(
        child=serializers.UUIDField()
    )

