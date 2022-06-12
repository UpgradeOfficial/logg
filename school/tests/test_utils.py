from django.test import TestCase
import os
from django.core import mail
from unittest import mock
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.conf import settings

from core.tests.models_setups import create_test_student


# Create your tests here.
@mock.patch('core.authentication.TokenAuthentication.authenticate')
class TestPrescription(TestCase):
    
    def setUp(self):
        self.student = create_test_student()
        
        
    

    def test_pharmacy_suggestion_via_email_with_prescription(self, authenticate_function):
        authenticate_function.return_value = self.student.user, None
        image_data = File(open(os.path.join(settings.BASE_DIR,'media','default.png'), 'rb'))
        image = SimpleUploadedFile("media/file.default.png", image_data.read(),content_type='multipart/form-data')
        data= { 
            'file':image,
              "email_dict": """{
                    "subject": "string",
                    "email": "user@example.com",
                    "name": "string",
                    "text": "string"
                }"""
            }
        url = reverse('school:send-email-with-attachment')
        response = self.client.post(url, data=data)
        res = response.json()
        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, f"File sent to {self.student.user.email}")
        self.assertEqual(mail.outbox[0].from_email,  settings.EMAIL_HOST_USER)
        self.assertEqual(mail.outbox[0].to,  [self.student.user.email])
        
