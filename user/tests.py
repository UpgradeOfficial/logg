from unittest import mock
import json
from django.test import TestCase
from django.urls import reverse
from core.utils import jwt_encode



from user.models import User

# Create your tests here.
class TestUser(TestCase):

    def setUp(self):
        #this is needed to hash the password
        #create user will not hash the password
        self.user = User.objects.create_user(email="odeyemiincrease@yahoo.c", password='password')

    def test_password_reset_with_email_that_exists(self):
        url = reverse("user:password_reset")
        data= {"email": self.user.email}
        response = self.client.post(url, data)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['message'], "email sent")

    def test_password_reset_with_wrong_email(self):
        url = reverse("user:password_reset")
        data= {"email": "emaildoesntexist@gmail.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    @mock.patch('core.authentication.TokenAuthentication.authenticate')
    def test_password_change_with_authenticated_user(self, authenticate_function):
        authenticate_function.return_value = self.user, None
        url = reverse("user:change_password")
        old_password = 'password'
        new_password = "new_password"
        data= {"old_password": old_password , "new_password": new_password }
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.first().check_password(new_password))
    
    @mock.patch('core.authentication.TokenAuthentication.authenticate')
    def test_password_change_with_unauthenticated_user_with_wrong_old_password(self, authenticate_function):
        authenticate_function.return_value = self.user, None
        url = reverse("user:change_password")
        old_password = 'wrong_old_password'
        new_password = "new_password"
        data= {"old_password": old_password , "new_password": new_password }
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.first().check_password(new_password))
        response_data = response.json()
        self.assertEqual(response_data['non_field_errors'], ['The old password field is incorrect'])

    

        
    def test_reset_password_with_rigth_email(self): 
        token = jwt_encode({'email':self.user.email})
        url = reverse("user:reset_password", kwargs={'token':token})
        new_password = "new_password"
        data= { "password": new_password }
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.first().check_password(new_password))

    def test_reset_password_with_rigth_email(self): 
        token = jwt_encode({'email':"wrong_email@gmail.com"})
        url = reverse("user:reset_password", kwargs={'token':token})
        new_password = "new_password"
        data= { "password": new_password }
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertFalse(User.objects.first().check_password(new_password))
      
