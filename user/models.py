from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.


from core.models import CoreModel

from .managers import UserManager


class User(AbstractUser, CoreModel):
    class AUTH_PROVIDER_TYPE(models.TextChoices):
        EMAIL = "EMAIL", _("email")
        GOOGLE = "GOOGLE", _("google")
        FACEBOOK = "FACEBOOK", _("facebook")
        TWITTER = "TWITTER", _("twitter")
        
    email = models.EmailField(_('email address'), unique=True)
    is_verified = models.BooleanField(default=False)
    auth_povider = models.CharField( _("user type"),
        max_length=20,
        choices=AUTH_PROVIDER_TYPE.choices,
        default=AUTH_PROVIDER_TYPE.EMAIL,
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

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)