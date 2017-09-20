from django.views.static import serve
from django.http import Http404, HttpResponse

from cotidia.file.utils.variation import generate_variation
from cotidia.file.conf import settings
from cotidia.file.models import File


def serve_variation_dev(request, path, document_root=None, show_indexes=False):
    try:
        return serve(request, path, document_root, show_indexes)
    except Http404:
        return serve_variation(request, path)


def serve_variation(request, path):

    path_parts = path.split("/")
    variation = path_parts[-2]
    file_name = path_parts[-1]

    if variation not in settings.FILE_IMAGE_VARIATIONS.keys():
        raise Http404("Variation '{}' does not exist.".format(variation))

    try:
        f = File.objects.get(name=file_name)
    except File.DoesNotExist:
        raise Http404

    # Check that the path is valid
    expected_path = f.build_variation_path(variation)
    if expected_path != path:
        raise Http404("Invalid path")

    # File must be an image to be generated
    if not f.is_image:
        raise Http404
    else:
        new_file = generate_variation(f, variation)
        return HttpResponse(new_file.read(), content_type=f.mimetype)
