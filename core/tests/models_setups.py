from datetime import date
from django.test import TestCase
from core.utils import random_with_N_digits
from school.models import ClassRoom, Term
from user.models import School, Student, Teacher, User
# Create your tests here.

def create_test_user(email=None, password=None, user_type=None, nop=10):
    random=random_with_N_digits(nop)
    if not password:
        password = random
    if not email:
        email = f"email{random}@gmail.com"
    if not user_type:
        user_type = User.USER_TYPE.STUDENT
    return User.objects.create_user(email=email, password=str(password), user_type=user_type)


def create_test_school(name=None, user=None, nop=10):
    random=random_with_N_digits(nop)
    if not name:
        name = random
    if not user:
        user = create_test_user(user_type=User.USER_TYPE.SCHOOL)
    return School.objects.create(user=user, name=name)

def create_test_teacher(user=None, school=None):
    if not user:
        user = create_test_user()
    if not school:
        school = create_test_school()
    
    return Teacher.objects.create(user=user, school=school)

def create_test_student(user=None):
    if not user:
        user = create_test_user()
    
    return Student.objects.create(user=user)

def create_test_class_room(name=None, school=None, teacher = None):
    '''
    the name of the class defaults to primary 1
    '''
    if not school:
        school = create_test_school()
    if not name:
        name = "primary 1"
    if teacher=="leave":
        return ClassRoom.objects.create(name=name, school=school)
    if not teacher:
        teacher = create_test_teacher()
    return ClassRoom.objects.create(name=name, school=school, class_teacher= teacher)

def create_test_class_teacher(classroom=None, teacher=None):
    
    if not classroom:
        classroom = create_test_class_room()
    if teacher:
        teacher = create_test_teacher()
    classroom.class_teacher = teacher
    result = classroom.save()

    return result

def create_test_term(name=None, school=None, start_date=None, end_date=None ):
    '''
    the name of the class defaults to primary 1
    '''
    if not school:
        school = create_test_school()
    if not name:
        name = "primary 1"
    if not start_date:
        start_date = date.today()
    if not end_date:
        end_date = date.today() 
    return Term.objects.create(name=name, school=school, start_date=start_date, end_date=end_date)