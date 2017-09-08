from cotidia.admin.views import AdminListView, AdminDeleteView

from cotidia.file.models import File


class FileList(AdminListView):
    columns = (
        ('Name', 'name'),
        ('Date Created', 'created_at'),
    )
    model = File


class FileDelete(AdminDeleteView):
    model = File
