
from django.urls  import reverse
from django.test import TestCase

from core.tests.models_setups import create_class_room, create_school
import school



#from user.models import Administrator, Guardian, School, Staff, Student, Teacher, User

# Create your tests here.

class TestSchool(TestCase):

    def setUp(self):
        self.school1 = create_school()
        self.school2 = create_school()
        

    def test_school_list_view(self):
        url = reverse("school:list_school")
        res = self.client.get(url)
        res_json = res.json()
        self.assertEqual(len(res_json['results']), 2)

    # NOt tested
    def test_school_classroom_list_view(self):
        url = reverse("school:list_school_classroom", kwargs={'pk':self.school1.id})
        classroom1 = create_class_room(school=self.school1)
        classroom2 = create_class_room(school=self.school1)
        classroom3 = create_class_room(school=self.school1)
        res = self.client.get(url)
        res_json = res.json()
        self.assertEqual(len(res_json['results']), 3)

    def test_school_classroom_list_view(self):
        url = reverse("school:list_school_classroom", kwargs={'pk':self.school1.id})
        classroom1 = create_class_room(school=self.school1)
        classroom2 = create_class_room(school=self.school1)
        classroom3 = create_class_room(school=self.school1)
        res = self.client.get(url)
        res_json = res.json()
        self.assertEqual(len(res_json['results']), 3)
        
