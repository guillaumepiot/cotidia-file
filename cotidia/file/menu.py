from django.core.urlresolvers import reverse


def admin_menu(context):
    return [
        {
            "icon": "file",
            "text": "Files",
            "url": reverse("file-admin:file-list")
        }
    ]
