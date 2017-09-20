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

## Commands

### Generate image variations for all files

Command: `generate_image_variations`

Example:

```console
$ python manage.py generate_image_variations
```

## Maintenance

The test suite must be run after all code update.

```console
$ python runtests.py
```
