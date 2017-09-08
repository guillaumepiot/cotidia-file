import magic

from django.template.defaultfilters import filesizeformat
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
            'content_type',
            'object_id',
            'taxonomy',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'uuid',
            'name',
            'mimetype',
            'created_at',
            'updated_at'
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
