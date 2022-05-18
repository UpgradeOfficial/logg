
from django.test import TestCase
from django.urls import reverse

from user.models import School, Student, User

# Create your tests here.
class TestContactUs(TestCase):

    def test_contact_us(self):
        
        data = {
            "name":"increase",
            "email": "odeyemiincrease@yahoo.com",
            "subject":"Cmplain",
            "text":"this is a random text"
        }
        url = reverse("core:contact_us")
        res = self.client.post(url, data=data, content_type='application/json')
        res_json = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res_json['message'],"You message has been received and is been processed.")