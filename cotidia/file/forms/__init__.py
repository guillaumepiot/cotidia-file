from betterforms.forms import BetterModelForm

from cotidia.file.models import File


class FileAddForm(BetterModelForm):

    class Meta:
        model = File
        fields = ['f', 'public', 'title', 'alt_tags']
        fieldsets = (
            ('upload', {
                'fields': (
                    'f',
                    'public'
                ),
                'legend': 'Upload'
            }),
            ('info', {
                'fields': (
                    "title",
                    "alt_tags",
                ),
                'legend': 'File details'
            }),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['f'].label = "File"


class FileUpdateForm(BetterModelForm):

    class Meta:
        model = File
        fields = ['f', 'alt_tags', 'title']
        fieldsets = (
            ('upload', {
                'fields': (
                    "f",
                ),
                'legend': 'Upload'
            }),
            ('info', {
                'fields': (
                    "alt_tags",
                    "title",
                ),
                'legend': 'File details'
            }),
        )
