from venv import create
from .models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        pass
        # send_mail('Subject here','Here is the message.','from@example.com', 
        #     [instance.email],  fail_silently=False,)
    