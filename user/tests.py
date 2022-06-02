import os
from unittest import mock
from django.core.files import File
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse
from django.contrib.sites.models import Site
from django.core import mail
from core.tests.models_setups import create_test_class_room, create_test_school, create_test_user
from core.utils import ExpiringActivationTokenGenerator, jwt_encode
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from user.models import Administrator, Guardian, School, Staff, Student, Teacher, User

# Create your tests here.

class TestUserRegistration(TestCase):

    def setUp(self):
        #this is needed to hash the password
        #create user will not hash the password
        # self.user = User.objects.create_user(email="odeyemiincrease@yahoo.c", password='password')
        self.user = create_test_user() # 1 user

    def test_student_registration_right_information(self):
        classroom = create_test_class_room() # create a teacher, teacher also create school , and a school 3 user 
        school = classroom.school
        image_data = File(open(os.path.join(settings.BASE_DIR,'media','default.png'), 'rb'))
        image = SimpleUploadedFile("media/file.default.png", image_data.read(),content_type='multipart/form-data')
        url = reverse("user:register")
        data= {"email":"i@i.com", "password": "new_password", 'image':image}
        response = self.client.post(url, data=data)
        response_dict = response.json()
        self.assertEqual(response.status_code, 201)
        student = Student.objects.first()
        # users are school, student, setup user
        self.assertEqual(User.objects.count(),5)
        self.assertEqual(Student.objects.count(),1)
        self.assertTrue(User.objects.filter(email="i@i.com").exists())
        self.assertTrue('tokens' in response_dict)
        self.assertTrue('access' in response_dict["tokens"])
        self.assertTrue('refresh' in response_dict["tokens"])
        link = (
            "/".join(
                [
                    settings.FRONTEND_URL,
                    "api",
                    "user"
                    "email-verification",
                    ExpiringActivationTokenGenerator().generate_token(student.user.email).decode('utf-8')
                ]
            )
        )
        base_url =  settings.BACKEND_BASE_URL
        context = {
        "site": "Logg",
        "MEDIA_URL": "/".join((base_url, settings.MEDIA_URL[1:-1])),
        "name": student.user.first_name or student.user.email,
        "link": link   
        }
        template_name = "account_verification.html"
        email_html_body = render_to_string(template_name, context)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Welcome to Logg, please verify your email address")
        self.assertEqual(mail.outbox[0].from_email, settings.EMAIL_HOST_USER)
        self.assertEqual(mail.outbox[0].to[0], student.user.email)
        # with open('index.html', 'w') as f:
        #     f.write(mail.outbox[0].body)
        # print(mail.outbox[0].body)
        # self.assertTrue(ExpiringActivationTokenGenerator().generate_token(student.user.email).decode('utf-8') in mail.outbox[0].body )
        #self.assertEqual(mail.outbox[0].body, email_html_body)
        #check if password is hashed
        self.assertNotEqual(data['password'], User.objects.first().password)
   
        
    def test_school_registration_right_information(self):
        image_data = File(open(os.path.join(settings.BASE_DIR,'media','default.png'), 'rb'))
        image = SimpleUploadedFile("media/file.default.png", image_data.read(),content_type='multipart/form-data')
        url = reverse("user:register")
        data= {"email":"i@i.com", "password": "new_password", 'image':image, 'user_type':"SCHOOL"}
        response = self.client.post(url, data=data)
        response_dict = response.json()
        self.assertEqual(response.status_code, 201)
        school = School.objects.first()
        self.assertEqual(school.user.email, data.get('email'))

    def test_guardian_registration_right_information(self):
        data = File(open(os.path.join(settings.BASE_DIR,'media','default.png'), 'rb'))
        image = SimpleUploadedFile("media/file.default.png", data.read(),content_type='multipart/form-data')
        url = reverse("user:register")
        data= {"email":"i@i.com", "password": "new_password", 'image':image, 'user_type':"GUARDIAN"}
        response = self.client.post(url, data=data)
        response_dict = response.json()
        self.assertEqual(response.status_code, 201)
        guardian = Guardian.objects.first()
        self.assertEqual(guardian.user.email, data.get('email'))

    def test_teacher_registration_right_information(self):
        data = File(open(os.path.join(settings.BASE_DIR,'media','default.png'), 'rb'))
        school = create_test_school()
        image = SimpleUploadedFile("media/file.default.png", data.read(),content_type='multipart/form-data')
        url = reverse("user:register")
        data= {"email":"i@i.com", "password": "new_password", 'image':image, 'user_type':"TEACHER", "school":school.id}
        response = self.client.post(url, data=data)
        response_dict = response.json()
        self.assertEqual(response.status_code, 201)
        teacher = Teacher.objects.first()
        self.assertEqual(teacher.user.email, data.get('email'))
        self.assertEqual(teacher.school, school)

    def test_administrator_registration_right_information(self):
        data = File(open(os.path.join(settings.BASE_DIR,'media','default.png'), 'rb'))
        school = create_test_school()
        image = SimpleUploadedFile("media/file.default.png", data.read(),content_type='multipart/form-data')
        url = reverse("user:register")
        data= {"email":"i@i.com", "password": "new_password", 'image':image, 'user_type':"ADMINISTRATOR", "school":school.id}
        response = self.client.post(url, data=data)
        response_dict = response.json()
        self.assertEqual(response.status_code, 201)
        administrator = Administrator.objects.first()
        self.assertEqual(administrator.user.email, data.get('email'))
        self.assertEqual(administrator.school, school)

    def test_staff_registration_right_information(self):
        data = File(open(os.path.join(settings.BASE_DIR,'media','default.png'), 'rb'))
        image = SimpleUploadedFile("media/file.default.png", data.read(),content_type='multipart/form-data')
        url = reverse("user:register")
        data= {"email":"i@i.com", "password": "new_password", 'image':image, 'user_type':"STAFF"}
        response = self.client.post(url, data=data)
        response_dict = response.json()
        self.assertEqual(response.status_code, 201)
        staff = Staff.objects.first()
        self.assertEqual(staff.user.email, data.get('email'))

    def test_user_registration_email_in_database(self):
        data = File(open(os.path.join(settings.BASE_DIR,'media','default.png'), 'rb'))
        image = SimpleUploadedFile("media/file.default.png", data.read(),content_type='multipart/form-data') 
        url = reverse("user:register")
        data= {"email":self.user.email, "password": "new_password", "image": image}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(),1)
        self.assertFalse(User.objects.filter(email="i@i.com").exists())

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
        old_password = self.user.email.split('@')[0][5:]
        new_password = "new_password"
        data= {"old_password": old_password , "new_password": new_password }
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.first().check_password(new_password))
    
    @mock.patch('core.authentication.TokenAuthentication.authenticate')
    def test_password_change_with_authenticated_user_with_wrong_old_password(self, authenticate_function):
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

    def test_reset_password_with_wrong_email(self): 
        token = jwt_encode({'email':"wrong_email@gmail.com"})
        url = reverse("user:reset_password", kwargs={'token':token})
        new_password = "new_password"
        data= { "password": new_password }
        response = self.client.patch(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertFalse(User.objects.first().check_password(new_password))

    def test_email_verification_with_rigth_email(self): 
        token = ExpiringActivationTokenGenerator().generate_token(self.user.email).decode('utf-8')
        self.assertFalse(User.objects.first().is_verified)
        url = reverse("user:confirm_email", kwargs={'token':token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.first().is_verified)

class TestUser(TestCase):

    def setUp(self):
        
        self.user1 = create_test_user() 
        self.user2 = create_test_user() 
        self.user3= create_test_user() 
        self.user4 = create_test_user() 
        self.user = create_test_user() 

    def test_query_all_user(self): 
        url = reverse("user:user-list")
        response = self.client.get(url)
        response_dict = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_dict['results']), 5)

    def test_query_user_with_query_string(self): 
        url = reverse("user:user-list")
        query_params = {'email': self.user.email}
        response = self.client.get(url, query_params)
        response_dict = response.json()
        # # users are school, student, setup user
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_dict['results']), 1)
        self.assertEqual(response_dict['results'][0]['email'], query_params['email'])


class UploadStudentData(TestCase):
    def test_get_student_data_csv(self):
        url = reverse("user:upload-student-data")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'text/csv')

    def test_post_student_data_csv(self):
        url = reverse("user:upload-student-data")
        path_to_student_csv_file = os.path.join(settings.BASE_DIR, 'templates', 'test','student-upload.csv')
        data = open(path_to_student_csv_file, "rb")
        data = SimpleUploadedFile(
                content=data.read(), name=data.name, content_type="multipart/form-data"
            )

        # image_data = File(open(os.path.join(settings.BASE_DIR,'media','default.png'), 'rb'))
        # image = SimpleUploadedFile("media/file.default.png", image_data.read(),content_type='multipart/form-data')
        data  ={'file':data}
            # Perform put request (Act)
        response = self.client.post(url, data=data)
        response_dict = response.json()
        student = Student.objects.first()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_dict['message'], "Student Data Uploaded Successfully")
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(student.user.first_name, 'increase')
        self.assertEqual(student.user.last_name, 'odeyemi')
        self.assertEqual(student.user.email, f'increase_odeyemi@logg_student.com')
        self.assertTrue(User.objects.first().check_password('increase_odeyemi'))
        self.assertTrue(student.user.is_verified)
        
       
        

    
      
