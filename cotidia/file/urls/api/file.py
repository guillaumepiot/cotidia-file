from django.conf.urls import url

from cotidia.file.views.api.file import (
    Upload
    )

urlpatterns = [
    url(
        r'^upload$',
        Upload.as_view(),
        name="upload"),
    ]
