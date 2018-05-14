import os

from cotidia.file.conf import settings


def get_file_path(instance, filename):

    if settings.FILE_ENCRYPT_FILENAME:
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (instance.uuid, ext.lower())

    return os.path.join(settings.FILE_UPLOAD_PATH, filename)
