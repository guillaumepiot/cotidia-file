# Cotidia File

File upload handling for the Cotidia ecosystem.

## Install

Add `cotidia.file`to `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    ...
    'cotidia.file',
    ...
)
```

Add the API endpoints to your project URLs:

```python
from django.conf.urls import include, url

urlpatterns = [
    url(
        r'^api/file/',
        include('cotidia.file.urls.api.file', namespace="file-api")
    ),
]
```

## Settings

### `FILE_UPLOAD_PATH`

- Type: *String*
- Default: `"uploads/"`

Defines the path after Django's `MEDIA_ROOT` where the files should be uploaded.

### `FILE_ALLOWED_TYPES`

- Type: *List*
- Default: `[]`

Defines the list of allowed mimetypes, for example: `['application/pdf', 'text/plain']`. An empty list would allow all mimetypes.

### `FILE_MAX_UPLOAD_SIZE`

- Type: *Integer*
- Default: `4194304`

Defines the list of maximum file size for upload in bytes.

### `FILE_IMAGE_VARIATIONS`

Define image variations for image upload. All variations are generated on save.

Options:

- "crop" cut the largest portion of the image fitting in the crop size
- "thumbnail" reduce the file size to fit within the width and height

Format: [`action_type`, `width`, `height`]

```
FILE_IMAGE_VARIATIONS = {
    "thumbnail": ["crop", 100, 100],
    "small": ["resize", 100, 100]
}
```

### `FILE_RASTER_IMAGE_FORMATS`

Define which image type will be accepted to create variations. Essentially
any image that can be rasterized.

```
FILE_RASTER_IMAGE_FORMATS = [
    "image/gif",
    "image/jpeg",
    "image/png",
]
```

### `PUBLIC_FILE_STORAGE`

Define a django storage class for file upload that should be stored on a
public container. If the file request passes `public=True` then this storage
class will be used.


## Commands

### Generate image variations for all files

Command: `generate_image_variations`

Example:

```console
$ python manage.py generate_image_variations
```

### Set file order IDs

Command: `set_file_order_ids`

Example:

```console
$ python manage.py set_file_order_ids
```

## Maintenance

The test suite must be run after all code update.

```console
$ python runtests.py
```
