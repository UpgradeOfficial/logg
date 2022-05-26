from django.utils import timezone
from datetime import date
import logging
from django.urls  import reverse
from django.test import TestCase
from unittest import mock

from core.tests.models_setups import create_class_room, create_class_teacher, create_school, create_student, create_teacher, create_term, create_user
from school.models import ClassRoom, ClassRoomAttendance, Expense, Fee, Subject, Term
from user.models import Student
logger = logging.getLogger("debug")



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
        self.assertEqual(res.status_code, 200)
        res_json = res.json()
        self.assertEqual(len(res_json['results']), 3)
        

class TestClassRoom(TestCase):

    def setUp(self):
        self.user = create_user()
        self.school1 = create_school()
        self.school2 = create_school()
        
    @mock.patch('core.authentication.TokenAuthentication.authenticate')
    def test_create_classroom(self, authenticate_function):
        authenticate_function.return_value = self.school1.user, None
        url = reverse("school:create_classroom")
        data = {
            "school":self.school1.id,
            "name": "primary 1"
        }
        res = self.client.post(url, data=data)
        res_json = res.json()
        self.assertEqual(res.status_code, 201)
        classroom = ClassRoom.objects.first()
        self.assertEqual(classroom.school, self.school1)
        self.assertNotEqual(classroom.school, self.school2)

    @mock.patch('core.authentication.TokenAuthentication.authenticate')
    def test_get_classroom(self, authenticate_function):
        authenticate_function.return_value = self.school1.user, None
        classroom1 = create_class_room(name="Primary 1", school=self.school1, teacher = "leave")
        classroom2 = create_class_room(name="Primary 2", school=self.school1, teacher = "leave")
        classroom3 = create_class_room(name="Primary 3", school=self.school1, teacher = "leave")
        classroom4 = create_class_room(name="Primary 3", school=self.school2, teacher = "leave")
        url = reverse("school:create_classroom")
        res = self.client.get(url)
        res_json = res.json()
        self.assertEqual(res.status_code, 200)
        classroom = ClassRoom.objects.get(id=classroom1.id)
        self.assertEqual(len(res_json['results']), 3)
        self.assertNotEqual(classroom.school, self.school2)
        self.assertEqual(classroom.school, self.school1)
        self.assertNotEqual(classroom.school, self.school2)


class TestTerm(TestCase):
        
    @mock.patch('core.authentication.TokenAuthentication.authenticate')
    def test_create_term(self, authenticate_function):
        school1 = create_school()
        authenticate_function.return_value = school1.user, None
        url = reverse("school:create_term")
        data = {
            "school":school1.id,
            "name": Term.TERM_TYPE.FIRST,
            'start_date': date.today(),
            'end_date': date.today()
        }
        res = self.client.post(url, data=data)
        res_json = res.json()
        self.assertEqual(res.status_code, 201)
        term = Term.objects.first()
        self.assertEqual(term.school, school1)
        self.assertEqual(term.name, data.get('name'))
        self.assertEqual(term.start_date, data.get('start_date'))

class TestExpense(TestCase):
        
    @mock.patch('core.authentication.TokenAuthentication.authenticate')
    def test_create_expense(self, authenticate_function):
        school1 = create_school()
        term = create_term(school=school1)
        authenticate_function.return_value = school1.user, None
        url = reverse("school:create_expense")
        data = {
            "term":term.id,
            "name": 'Expense.expense_TYPE.FIRST',
            'amount': 2000
        }
        res = self.client.post(url, data=data)
        res_json = res.json()
        self.assertEqual(res.status_code, 201)
        expense = Expense.objects.first()
        self.assertEqual(expense.term, term)
        self.assertEqual(expense.name, data.get('name'))
        self.assertEqual(expense.amount, data.get('amount'))

class TestClassRoomAttendance(TestCase):
        
    @mock.patch('core.authentication.TokenAuthentication.authenticate')
    def test_create_classroomattendance(self, authenticate_function):
        classroom_teacher = create_teacher()
        classroom = create_class_room(teacher=classroom_teacher)
        Student1 = create_student()
        Student2 = create_student()
        Student3 = create_student()
        Student4 = create_student()
        Student5 = create_student()
        authenticate_function.return_value =classroom_teacher.user, None

        url = reverse("school:create_classroom_attendance")
        data = {
            "classroom":classroom.id,
            "students":[Student1, Student2, Student3, Student4] 
        }
        res = self.client.post(url, data=data)
        res_json = res.json()
        self.assertEqual(res.status_code, 201)
        classroomattendance = ClassRoomAttendance.objects.first()
        self.assertEqual(classroomattendance.students.count(), 4)
        self.assertIn(Student1, classroomattendance.students.all())
        self.assertNotIn(Student5, classroomattendance.students.all())

    

class TestSubject(TestCase):

        
    @mock.patch('core.authentication.TokenAuthentication.authenticate')
    def test_create_subject(self, authenticate_function):
        self.school1 = create_school()
        authenticate_function.return_value = self.school1.user, None
        classroom = create_class_room(school=self.school1)
        url = reverse("school:create_subject")
        data = {
            "classroom": classroom,
            "name": "primary 1"
        }
        res = self.client.post(url, data=data)
        res_json = res.json()
        # logger.debug(res_json)
        self.assertEqual(res.status_code, 201)
        
class TestFee(TestCase):

        
    @mock.patch('core.authentication.TokenAuthentication.authenticate')
    def test_create_fee(self, authenticate_function):
        school1 = create_school()
        term = create_term(school=school1)
        authenticate_function.return_value = school1.user, None
        url = reverse("school:create_fee")
        data = {
            "term": term,
            "name": "school Fee",
            "amount":1000
        }
        res = self.client.post(url, data=data)
        res_json = res.json()
        fee = Fee.objects.first()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(fee.amount, 1000)
        self.assertEqual(fee.name, data['name'])