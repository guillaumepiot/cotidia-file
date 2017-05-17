import os

from django.template.defaultfilters import filesizeformat
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase

from cotidia.core.utils.doc import Doc
from cotidia.file.utils.generator import (
    generate_pdf_file,
    generate_text_file,
    generate_image_file
)
from cotidia.file.models import File
from cotidia.file.conf import settings
from cotidia.file.tests.models import GenericItem


class FileAPITests(APITestCase):

    maxDiff = None
    display_doc = True

    def setUp(self):
        self.doc = Doc()

        # Test settings
        settings.FILE_MAX_UPLOAD_SIZE = 1600  # 1.6kb
        settings.FILE_ALLOWED_TYPES = ['application/pdf']

        # Create a generic item to test the generic foreign key
        self.item = GenericItem.objects.create()

    def tearDown(self):
        # Clean up uploaded files
        if File.objects.filter():
            f = File.objects.filter().latest("id")
            os.remove(f.f.path)
            os.rmdir(
                os.path.join(
                    os.path.dirname(__file__),
                    '../../../../%s' % settings.FILE_UPLOAD_PATH
                    )
                )

    def test_upload_file(self):
        """Test if we can upload a photo."""

        # self.client.credentials(
        #     HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)

        url = reverse('file-api:upload')

        pdf_file = generate_pdf_file()

        data = {
            'f': pdf_file
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "test.pdf")
        self.assertEqual(response.data["mimetype"], "application/pdf")

        if self.display_doc:
            payload = data.copy()
            payload['f'] = "test.pdf"
            content = {
                'title': "Upload file",
                'url': url,
                'http_method': 'POST',
                'payload': payload,
                'response': response.data
            }
            self.doc.display_section(content)

    def test_upload_file_with_generic_relation(self):
        """Test if we can upload a photo."""

        # self.client.credentials(
        #     HTTP_AUTHORIZATION='Token ' + self.normal_user_token.key)

        url = reverse('file-api:upload')

        pdf_file = generate_pdf_file()
        content_type_id = ContentType.objects.get_for_model(self.item).id

        data = {
            'f': pdf_file,
            'content_type': content_type_id,
            'object_id': self.item.id
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "test.pdf")
        self.assertEqual(response.data["mimetype"], "application/pdf")
        self.assertEqual(response.data["content_type"], content_type_id)
        self.assertEqual(response.data["object_id"], self.item.id)

        if self.display_doc:
            payload = data.copy()
            payload['f'] = "test.pdf"
            content = {
                'title': "Upload file with generic relation",
                'url': url,
                'http_method': 'POST',
                'payload': payload,
                'response': response.data
            }
            self.doc.display_section(content)

    def test_file_type_validation(self):
        """Test if we get a validation error for invalid file types."""

        url = reverse('file-api:upload')

        text_file = generate_text_file()

        data = {
            'f': text_file
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['f'],
            ['File type (text/plain) is invalid.']
            )

    def test_file_filesize_validation(self):
        """Test if we get a validation error for large files."""

        url = reverse('file-api:upload')

        # Make a larger image so it exceeds the file size limit on purpose
        pdf_file = generate_pdf_file(content="Some text " * 5000)

        data = {
            'f': pdf_file
        }

        max_upload_size_fmt = filesizeformat(settings.FILE_MAX_UPLOAD_SIZE)

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['f'],
            [
                'File size too large. It must be less than {}'\
                .format(max_upload_size_fmt)
            ]
            )
