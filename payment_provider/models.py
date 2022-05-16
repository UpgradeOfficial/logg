from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import CoreModel

# Create your models here.
class PaymantProvider(models.TextChoices):
    PAYSTACK = "T", _("paystack")
    FLUTTERWAVE = "F", _("flutterwave")


class Payment(CoreModel):
    name = models.CharField(max_length=100)
    fee = models.ForeignKey("school.Fee", on_delete=models.PROTECT)
    payment_provider = models.CharField( _("Payment Provider"),
        max_length=20,
        choices=PaymantProvider.choices,
        blank=True,
        null=True
    )
    amount = models.DecimalField(decimal_places=2, max_digits=30)
    student = models.ForeignKey('user.Student', on_delete=models.PROTECT)
    