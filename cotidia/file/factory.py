import factory

from cotidia.file.models import File


class FileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = File

    f = factory.django.FileField(filename='test.pdf')
