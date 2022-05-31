
from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from core.utils import send_mail
# Create your models here.


from core.models import CoreModel, CoreUserModel
from core.utils import ExpiringActivationTokenGenerator

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

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def send_email_verification_mail(self):
        template = "account_verification.html"

        confirmation_token = ExpiringActivationTokenGenerator().generate_token(
            text=self.email
        )

        link = (
            "/".join(
                [
                    settings.FRONTEND_URL,
                    "api",
                    "user"
                    "confirm_email",
                    confirmation_token.decode('utf-8')
                ]
            )
        )
        send_mail(
            to_email=self.email,
            subject=f"Welcome to Logg, please verify your email address",
            template_name=template,
            input_context={
                "name": self.first_name or self.email,
                "link": link
            },
        )

    

class School(CoreModel, CoreUserModel):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}_{self.user.email}_{self.user.user_type}"

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
    
    
class Staff(CoreModel, CoreUserModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)