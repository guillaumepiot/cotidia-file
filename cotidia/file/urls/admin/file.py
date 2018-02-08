from django.urls import path

from cotidia.file.views.admin.file import (
    FileList,
    FileDetail,
    FileDelete
)

urlpatterns = [
    path(
        '',
        FileList.as_view(),
        name='file-list'),
    path(
        '<pk>',
        FileDetail.as_view(),
        name='file-detail'),
    path(
        '<pk>/delete',
        FileDelete.as_view(),
        name='file-delete'),
]
