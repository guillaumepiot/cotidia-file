from django.conf.urls import url

from cotidia.file.views.api.file import (
    Upload,
    Reorder
)

app_name = 'cotidia.file'

urlpatterns = [
    url(
        r'^upload$',
        Upload.as_view(),
        name="upload"),
    url(
        r'^reorder$',
        Reorder.as_view(),
        name="reorder"),
]
