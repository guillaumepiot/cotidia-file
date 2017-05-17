# Cotidia file

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

## Settings

`UPLOAD_PATH`: Defines the path after Django's `MEDIA_ROOT` where the files should be uploaded.
