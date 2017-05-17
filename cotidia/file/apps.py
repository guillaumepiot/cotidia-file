from django.apps import AppConfig


class FileConfig(AppConfig):
    name = "cotidia.file"
    label = "file"

    def ready(self):
        import cotidia.file.signals
