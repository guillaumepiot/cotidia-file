import uuid
import django_filters
from cotidia.file.models import File
from cotidia.file.forms import FileAddForm, FileUpdateForm
from django.db.models import Q

from cotidia.admin.views import (
    AdminListView,
    AdminDetailView,
    AdminCreateView,
    AdminDeleteView,
    AdminUpdateView
)

from cotidia.file.models import File


class FileFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        label="Search",
        method="search"
    )

    class Meta:
        model = File
        fields = ['name']

    def search(self, queryset, name, value):

        q_objects = Q(name__icontains=value) | \
            Q(taxonomy__icontains=value)

        try:
            val = uuid.UUID(value, version=4)
            q_objects |= Q(uuid=val)
        except ValueError:
            pass

        return queryset.filter(q_objects)


class FileList(AdminListView):
    columns = (
        ('Name', 'name'),
        ('Date Created', 'created_at'),
    )
    model = File
    row_actions = ['view', 'update', 'delete']
    row_click_action = 'detail'
    filterset = FileFilter


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
                [
                    {
                        "label": "Date Created",
                        "field": "created_at",
                    },
                    {
                        "label": "File url",
                        "field": "f.url",
                    },
                ],
                [
                    {
                        "label": "MIME type",
                        "field": "mimetype",
                    },
                    {
                        "label": "Public",
                        "field": "public",
                    },
                ],
                {
                    "label": "Title",
                    "field": "title",
                },
                {
                    "label": "Alt tags",
                    "field": "alt_tags",
                },

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


class FileCreate(AdminCreateView):
    model = File
    form_class = FileAddForm


class FileUpdate(AdminUpdateView):
    model = File
    form_class = FileUpdateForm


class FileDelete(AdminDeleteView):
    model = File
