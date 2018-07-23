from betterforms.forms import BetterModelForm

from cotidia.file.models import File


class FileUpdateForm(BetterModelForm):

    class Meta:
        model = File
        fields = ['alt_tags', 'title']
        fieldsets = (
            ('info', {
                'fields': (
                    "title",
                    "alt_tags",
                ),
                'legend': 'File details'
            }),
        )
