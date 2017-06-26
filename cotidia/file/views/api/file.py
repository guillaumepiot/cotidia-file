from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied

from cotidia.file.serializers import FileSerializer


class Upload(generics.CreateAPIView):
    allowed_methods = ('post',)
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def post(self, request, *args, **kwargs):
        # Make sure the admin user also has uploading permissions
        if request.user.is_authenticated() \
                and not request.user.has_perm("file.add_file"):
            raise PermissionDenied

        return super().post(request, *args, **kwargs)
