from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from cotidia.file.serializers import FileSerializer
from cotidia.file.models import File

from django.core.exceptions import ValidationError


class Upload(generics.CreateAPIView):
    allowed_methods = ('post',)
    parser_classes = (MultiPartParser, FormParser,)
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def post(self, request, *args, **kwargs):
        # Make sure the admin user also has uploading permissions
        if request.user.is_authenticated \
                and not request.user.has_perm("file.add_file"):
            raise PermissionDenied

        return super().post(request, *args, **kwargs)


class Reorder(APIView):
    def post(self, request):
        uuids = request.data.getlist("data")
        # 1 required as order_ids must be > 0
        for i, uuid in enumerate(uuids, 1):
            try:
                file = File.objects.get(uuid=uuid)
            except File.DoesNotExist:
                return Response(status=404)
            except ValidationError:
                return Response(status=400)
            file.order_id = i
            file.save()
        return Response(status=200)

