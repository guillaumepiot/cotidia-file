from django.urls import include, path

app_name = 'file-admin'

urlpatterns = [
    path(
        '',
        include('cotidia.file.urls.admin.file')
    ),
]
