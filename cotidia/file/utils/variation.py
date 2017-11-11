import io

from PIL import Image

from django.core.files.base import ContentFile

from cotidia.file.conf import settings


def generate_variation(f, variation):
    action = settings.FILE_IMAGE_VARIATIONS[variation][0]
    size = settings.FILE_IMAGE_VARIATIONS[variation][1:3]
    file_type = f.mimetype.replace("image/", "")

    storage = f.get_storage()

    # Open original file in read-only mode
    try:
        fh = storage.open(f.f.name, "rb")
    except FileNotFoundError:
        return

    original_img = Image.open(fh)

    # Create a stream to generate the new file to
    temp_file = io.BytesIO()

    if action == "resize":
        original_img.thumbnail(size)
        original_img.save(temp_file, file_type)

    elif action == "crop":
        half_the_width = original_img.size[0] / 2
        half_the_height = original_img.size[1] / 2
        original_img.crop(
            (
                round(half_the_width - (size[0] / 2)),
                round(half_the_height - (size[1] / 2)),
                round(half_the_width + (size[0] / 2)),
                round(half_the_height + (size[1] / 2))
            )
        )
        original_img.thumbnail(size)
        original_img.save(temp_file, file_type)

    temp_file.seek(0)

    # Save the stream to a new file in storage
    new_path = f.build_variation_path(variation)
    storage.save(new_path, ContentFile(temp_file.read()))

    fh.close()
    temp_file.close()

    return storage.open(new_path, "rb")
