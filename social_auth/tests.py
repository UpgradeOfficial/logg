from django.urls import reverse
from django.test import TestCase

# Create your tests here.

class TestFacebookSocialAuthLogin(TestCase):

    def test_facebook(self):
        url = reverse("social_auth:facebook-login")
        data  = {
            'auth_token': "EAAHH3WhNZCYYBAO0For3TT4DUuViHpZBWHSFYX524Q9cDlcqhGla4ZApivcOxdoiNkZAudHFLLauur7bSzN56kdnlKxn2ZBQHUkUGTcDVUwWMhFF39dCGOI9xiXZCeRf8Lqs5ldFHPuQJ1hVfDqeXXCmpHufAXGSoswejcnrx4W3CoMYqL1iZBkKMu98ZBiZC5Tp9O8KKWFS8qtjUooZBv3hIy"
        }
        res = self.client.post(url, data=data)
        response_dict = res.json()
        print(response_dict)
