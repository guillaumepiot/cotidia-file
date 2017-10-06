from django.core.management.base import BaseCommand

from cotidia.file.models import File


class Command(BaseCommand):
    help = 'Generate image variations for all files.'

    def order_file_group(self):
        f = File.objects.filter(order_id=None).first()
        if f:
            # Get a group of file
            file_group = File.objects.filter(
                content_type=f.content_type,
                object_id=f.object_id
            )
            order_id = 0
            for f in file_group:
                f.order_id = order_id
                f.save()
                order_id += 1

            self.order_file_group()

        else:
            print("Complete!")

    def handle(self, *args, **options):
        self.order_file_group()
