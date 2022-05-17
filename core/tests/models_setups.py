from django.test import TestCase
from core.utils import random_with_N_digits
from school.models import ClassRoom
from user.models import School, User
# Create your tests here.

def create_user(email=None, password=None, nop=10):
    random=random_with_N_digits(nop)
    if not password:
        password = random
    if not email:
        email = f"email{random}@gmail.com"
    return User.objects.create_user(email=email, password=str(password))

def create_school(name=None, user=None, nop=10):
    random=random_with_N_digits(nop)
    if not name:
        name = random
    if not user:
        user = create_user()
    return School.objects.create(user=user, name=name)

def create_class_room(name=None, school=None):
    '''
    the name of the class defaults to primary 1
    '''
    if not school:
        school = create_school()
    if not name:
        name = "primary 1"
    return ClassRoom.objects.create(name=name, school=school)