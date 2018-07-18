from django import forms
from cotidia.file.models import File


class FileUpdateForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['alt_tags', 'title']
