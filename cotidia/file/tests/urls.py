from django.conf.urls import include, url

from cotidia.account.views.admin import dashboard
from .views import PublicUpload

urlpatterns = [
    url(r'^api/file/', include('cotidia.file.urls.api.file',
        namespace="file-api")),
    url(r'^api/file/upload-public$', PublicUpload.as_view(),
        name="file-upload-public"),
    url(r'^admin/file/', include('cotidia.file.urls.admin.file',
        namespace="file-admin")),
    url(r'^admin/account/', include('cotidia.account.urls.admin',
        namespace="account-admin")),
    url(r'^admin/mail/', include('cotidia.mail.urls',
        namespace="mail-admin")),
    url(
        r'^admin/$',
        dashboard,
        name="dashboard"
    ),
]
