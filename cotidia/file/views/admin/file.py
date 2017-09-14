from cotidia.admin.views import (
    AdminListView,
    AdminDetailView,
    AdminDeleteView
)

from cotidia.file.models import File


class FileList(AdminListView):
    columns = (
        ('Name', 'name'),
        ('Date Created', 'created_at'),
    )
    model = File


class FileDetail(AdminDetailView):
    model = File
    fieldsets = [
        {
            "legend": "File details",
            "fields": [
                [
                    {
                        "label": "Name",
                        "field": "name",
                    },
                    {
                        "label": "File path",
                        "field": "f",
                    },
                ],
                {
                    "label": "Date Created",
                    "field": "created_at",
                },
                {
                    "label": "MIME type",
                    "field": "mimetype",
                }
            ]
        },
        {
            "legend": "Categorisation",
            "fields": [
                {
                    "label": "Related to object",
                    "field": "content_object",
                },
                {
                    "label": "Taxonomy",
                    "field": "taxonomy",
                }
            ]
        },
        {
            "legend": "Preview",
            "template_name": "admin/file/file/preview.html"
        }

    ]


class FileDelete(AdminDeleteView):
    model = File
