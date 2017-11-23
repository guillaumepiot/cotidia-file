import logging

from django.utils.module_loading import import_string
from django.db.models.fields.files import FieldFile, FileField

from cotidia.file.conf import settings

logger = logging.getLogger(__name__)


class CustomFieldFile(FieldFile):
    def save(self, name, content, save=True):
        if self.instance.public:
            if hasattr(settings, "PUBLIC_FILE_STORAGE"):
                self.storage = import_string(settings.PUBLIC_FILE_STORAGE)()
            else:
                logger.warning("PUBLIC_FILE_STORAGE not set.")
        super().save(name, content, save=save)


class CustomFileField(FileField):
    attr_class = CustomFieldFile
