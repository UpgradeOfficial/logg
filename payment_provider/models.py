from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class PaymantProvider(models.TextChoices):
    PAYSTACK = "T", _("paystack")
    FLUTTERWAVE = "F", _("flutterwave")
    