from django.urls import path

from cotidia.file.views.admin.file import (
    FileList,
    FileDetail,
    FileDelete,
    FileUpdate
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
        '<pk>/update',
        FileUpdate.as_view(),
        name='file-update'),
    path(
        '<pk>/delete',
        FileDelete.as_view(),
        name='file-delete'),
]
