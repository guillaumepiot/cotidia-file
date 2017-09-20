from django.core.management.base import BaseCommand

from cotidia.file.models import File
from cotidia.file.conf import settings
from cotidia.file.utils.variation import generate_variation


class Command(BaseCommand):
    help = 'Generate image variations for all files.'

    def handle(self, *args, **options):

        if not settings.FILE_IMAGE_VARIATIONS:
            return

        for f in File.objects.all():
            if f.is_image:
                for variation in settings.FILE_IMAGE_VARIATIONS.keys():
                    try:
                        generate_variation(f, variation)
                    except FileNotFoundError:
                        self.stdout.write(
                            self.style.ERROR(
                                'Original file not found for "%s"' % f.name
                            )
                        )

                    self.stdout.write(
                        self.style.ERROR(
                            'Generted vairation "%s" for "%s"' % (variation, f.name)
                        )
                    )
