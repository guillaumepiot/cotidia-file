from django import template

from cotidia.file.models import File

register = template.Library()


@register.assignment_tag
def get_files_for_object(content_type_id, object_id):
    return File.objects.filter(
        content_type__id=content_type_id,
        object_id=object_id
    )
