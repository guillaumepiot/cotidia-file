from django.conf import settings

from appconf import AppConf


class FileConf(AppConf):

    UPLOAD_PATH = "uploads/"
    ALLOWED_TYPES = []  # Empty list will allow all
    MAX_UPLOAD_SIZE = 4194304  # 4MB

    IMAGE_VARIATIONS = {
        "thumbnail": ["crop", 100, 100],
        "small": ["resize", 100, 100]
    }

    class Meta:
        prefix = 'file'
