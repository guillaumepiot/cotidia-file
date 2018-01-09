from django.conf.urls import url

from cotidia.file.views.admin.file import (
    FileList,
    FileDetail,
    FileDelete
)

app_name = 'cotidia.file'

urlpatterns = [
    url(
        r'^$',
        FileList.as_view(),
        name='file-list'),
    url(
        r'^(?P<pk>[\d]+)$',
        FileDetail.as_view(),
        name='file-detail'),
    url(
        r'^(?P<pk>[\d]+)/delete$',
        FileDelete.as_view(),
        name='file-delete'),
]
