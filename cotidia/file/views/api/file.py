from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser

from cotidia.file.serializers import FileSerializer


class Upload(generics.CreateAPIView):
    allowed_methods = ('post',)
    parser_classes = (MultiPartParser, FormParser,)

    def get_serializer_class(self):
        return FileSerializer

    def get_permissions(self):
        return []
