from django import template

from cotidia.file.models import File

register = template.Library()


@register.simple_tag
def get_files_for_object(content_type_id, object_id):
    return File.objects.filter(
        content_type__id=content_type_id,
        object_id=object_id
    ).order_by('-created_at')


@register.simple_tag
def get_variation_url(object, variation):
    url = object.f.url
    url_parts = url.split("/")
    # Add the variation as the last folder in the url
    url_parts.insert(-1, variation)
    return "/".join(url_parts)
