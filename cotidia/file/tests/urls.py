from django.conf.urls import include, url

from .views import PublicUpload

urlpatterns = [
    url(r'^api/file/', include('cotidia.file.urls.api.file',
        namespace="file-api")),
    url(r'^api/file/upload-public$', PublicUpload.as_view(),
        name="file-upload-public"),
    url(r'^admin/file/', include('cotidia.file.urls.admin.file',
        namespace="file-admin")),
]
