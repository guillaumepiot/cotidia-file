import os, shutil

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission

from cotidia.file.models import File
from cotidia.file.factory import FileFactory
from cotidia.file.conf import settings


class FileAdminTests(TestCase):

    def setUp(self):

        # Create a default object, to use with update, retrieve, list & delete
        self.object = FileFactory.create()

        self.admin_user_permitted = User.objects.create(
            username="admin.permitted",
            email="admin.permitted@test.com",
            is_active=True,
            is_staff=True)
        self.admin_user_permitted.set_password("demo1234")
        self.admin_user_permitted.save()

        content_type = ContentType.objects.get_for_model(File)
        permission = Permission.objects.get(
            content_type=content_type, codename='delete_file')
        self.admin_user_permitted.user_permissions.add(permission)

        # Create the client and login the user
        self.c = Client()
        self.c.login(
            username="admin.permitted",
            password="demo1234")

    def tearDown(self):
        shutil.rmtree(os.path.join(
                os.path.dirname(__file__),
                '../../../../%s' % settings.FILE_UPLOAD_PATH
                )
            )

    def test_delete_file(self):
        """Test that we can delete an object."""

        url = reverse(
            'file-admin:file-delete',
            kwargs={
                'pk': self.object.id
                }
            )

        # Test that the page load first
        response = self.c.get(url)
        self.assertEqual(response.status_code, 200)

        # Action detail with POST call
        response = self.c.post(url)
        self.assertEqual(response.status_code, 302)

        # Test that the record has been deleted
        obj = File.objects.filter(id=self.object.id)
        self.assertEqual(obj.count(), 0)
