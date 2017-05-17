from django.conf import settings

from appconf import AppConf


class FileConf(AppConf):

    UPLOAD_PATH = "uploads/"
    ALLOWED_TYPES = []  # Empty list will allow all
    MAX_UPLOAD_SIZE = 4194304  # 4MB

    class Meta:
        prefix = 'file'
