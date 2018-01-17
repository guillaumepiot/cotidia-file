from django.conf.urls import url

from cotidia.file.views.api.file import (
    Upload,
    Order
)

app_name = 'cotidia.file'

urlpatterns = [
    url(
        r'^upload$',
        Upload.as_view(),
        name="upload"),
    url(
        r'^order/$',
        Order.as_view(),
        name="order"),
]
