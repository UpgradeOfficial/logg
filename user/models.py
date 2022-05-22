from email.policy import default
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.


from core.models import CoreModel, CoreUserModel

from .managers import UserManager
def upload_to(instance, filename):
    return "users/{filename}".format(filename=filename)

class User(AbstractUser, CoreModel):
    class AUTH_PROVIDER_TYPE(models.TextChoices):
        EMAIL = "EMAIL", _("email")
        GOOGLE = "GOOGLE", _("google")
        FACEBOOK = "FACEBOOK", _("facebook")
        TWITTER = "TWITTER", _("twitter")
    class USER_TYPE(models.TextChoices):
        SCHOOL = "SCHOOL", _("SCHOOL")
        ADMINISTRATOR = "ADMINISTRATOR", _("ADMINISTRATOR")
        TEACHER = "TEACHER", _("TEACHER")
        GUARDIAN = "GUARDIAN", _("GUARDIAN")
        STUDENT = "STUDENT", _("STUDENT")
        STAFF = "STAFF", _("STAFF")
        
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(_("image"), upload_to = upload_to, default="default.png")
    auth_povider = models.CharField( _("user type"),
        max_length=20,
        choices=AUTH_PROVIDER_TYPE.choices,
        default=AUTH_PROVIDER_TYPE.EMAIL,
        blank=True,
    )
    user_type = models.CharField( _("user type"),
        max_length=20,
        choices=USER_TYPE.choices,
        default=USER_TYPE.STUDENT,
        blank=True,
    )
    username = None
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self) -> str:
        return super().__str__()

    

class School(CoreModel, CoreUserModel):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Administrator(CoreModel, CoreUserModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    

class Teacher(CoreModel, CoreUserModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    
class Guardian(CoreModel, CoreUserModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ManyToManyField(School)

class Student(CoreModel, CoreUserModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    classroom = models.ForeignKey("school.Classroom", on_delete=models.CASCADE)
    
    
class Staff(CoreModel, CoreUserModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)