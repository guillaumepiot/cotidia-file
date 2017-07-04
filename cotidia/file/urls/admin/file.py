from django.conf.urls import url

from cotidia.file.views.admin.file import (
    FileList,
    FileDelete
)


urlpatterns = [
    url(
        r'^$',
        FileList.as_view(),
        name='file-list'),
    url(
        r'^(?P<pk>[\d]+)/delete$',
        FileDelete.as_view(),
        name='file-delete'),
]
