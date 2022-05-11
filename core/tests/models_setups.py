from django.test import TestCase
from core.utils import random_with_N_digits
from user.models import User
# Create your tests here.

def create_user(email=None, password=None, nop=10):
    random=random_with_N_digits(nop)
    if not password:
        password = random
    if not email:
        email = f"email{random}@gmail.com"
    return User.objects.create_user(email=email, password=str(password))