import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import random
from random import randint
from datetime import datetime, timedelta
import jwt

from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

def jwt_encode(payload):
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def jwt_decode(encoded_jwt):
    result = jwt.decode(encoded_jwt, settings.SECRET_KEY, algorithms=["HS256"])
    return result




def date_now_plus(days=365):
   mydate = datetime.now() + timedelta(days=days)
   return mydate
   
random_string = random.randint(1000, 9999)


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def send_mail(subject, to_email, input_context, template_name, cc_list=[], bcc_list=[]):
    """
    Send Activation Email To User
    """
    base_url = input_context.get("host_url", 'Site.objects.get_current().domain')

    context = {
        "site": "Logg",
        "MEDIA_URL": "/".join((base_url, settings.MEDIA_URL[:-1])),
        **input_context,
    }

    # render email text
    email_html_message = render_to_string(template_name, context)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=email_html_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
