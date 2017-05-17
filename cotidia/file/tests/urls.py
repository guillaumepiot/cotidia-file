from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/file/', include('cotidia.file.urls.api.file',
        namespace="file-api")),
]
