from django.utils.module_loading import import_string
from django.db.models.fields.files import FieldFile, FileField

from cotidia.file.conf import settings


class CustomFieldFile(FieldFile):
    def save(self, name, content, save=True):
        if self.instance.public:
            if not hasattr(settings, "PUBLIC_FILE_STORAGE"):
                raise Exception("PUBLIC_FILE_STORAGE not set.")
            self.storage = import_string(settings.PUBLIC_FILE_STORAGE)()
        super().save(name, content, save=save)


class CustomFileField(FileField):
    attr_class = CustomFieldFile
