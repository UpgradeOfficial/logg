from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.models import Site
import random
from cryptography.fernet import Fernet, InvalidToken
from random import randint
from datetime import datetime, timedelta
from rest_framework.exceptions import  ValidationError
import jwt


# from azure.storage.blob import generate_blob_sas, AccountSasPermissions, BlobServiceClient, BlobClient, ContainerClient, __version__
from datetime import datetime, timedelta

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
    base_url =  settings.BACKEND_BASE_URL
    
    context = {
        "site": "Logg",
        "MEDIA_URL": "/".join((base_url, settings.MEDIA_URL[1:-1])),
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

def send_mail_with_attachment(subject: str, to_email: list, file, input_context: str, template_name: str, cc_list=[], bcc_list=[]):
    """
    Send Activation Email To User
    """
    base_url =  settings.BACKEND_BASE_URL
    
    context = {
        "site": "Logg",
        "MEDIA_URL": "/".join((base_url, settings.MEDIA_URL[1:-1])),
        **input_context,
    }
    email_list =[]
    email_list+=to_email
    # render email text
    body = render_to_string(template_name, context)

    
    email = EmailMessage(subject=subject, body=body, from_email=settings.EMAIL_HOST_USER, to=to_email)
    email.attach(file.name,  file.read(), file.content_type)
    email.send()



class ExpiringActivationTokenGenerator:
    FERNET_KEY = settings.FERNET_KEY
    fernet = Fernet(FERNET_KEY)

    DATE_FORMAT = "%Y-%m-%d %H-%M-%S"
    EXPIRATION_DAYS = 3

    def _get_time(self):
        """Returns a string with the current UTC time"""
        return datetime.utcnow().strftime(self.DATE_FORMAT)

    def _parse_time(self, d):
        """Parses a string produced by _get_time and returns a datetime object"""
        return datetime.strptime(d, self.DATE_FORMAT)

    def generate_token(self, text):
        """Generates an encrypted token"""
        full_text = text + "|" + self._get_time()
        token = self.fernet.encrypt(bytes(full_text, encoding="utf-8"))
        return token

    def get_token_value(self, token):
        """Gets a value from an encrypted token.
        Returns None if the token is invalid or has expired.
        """
        try:
            value = self.fernet.decrypt(bytes(token, encoding="utf-8")).decode("utf-8")
            separator_pos = value.rfind("|")

            text = value[:separator_pos]
            token_time = self._parse_time(value[separator_pos + 1 :])

            if token_time + timedelta(self.EXPIRATION_DAYS) < datetime.utcnow():
                raise InvalidToken("Token expired.")
        except InvalidToken:
            raise ValidationError("Invalid token.")

        return text




####################################### unimplemented functions #################################################
# def upload_image_and_generate_image_url(file_name, file):
#     # Account Name
#     account_name='doktoteststore'
#     # Container Name
#     container_name='images'
#     # Blob Name
#     blob_name=file_name
#     # EndpointSuffix
#     EndpointSuffix="core.windows.net"
#     # Account_Key
#     account_key="pRupu5YVoRhviHjed02kWgA20mK4a468FSncBfQVgXOY950Jd4uOmt8bEtWRDuS5Rus4FzdlS++m+AStPLfa/w=="
#     #  connection string
#     connect_str = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix={EndpointSuffix}"
#     url = f"https://{account_name}.blob.{EndpointSuffix}/{container_name}/{blob_name}"
#     # Create the BlobServiceClient object which will be used to create a container client
#     blob_service_client = BlobServiceClient.from_connection_string(connect_str)
#     # create a blob instance
#     blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
#     # upload the blob
#     blob_client.upload_blob(file)
#     # shared_access_signature
#     sas_token = generate_blob_sas(
#         account_name=account_name,
#         account_key=account_key,
#         container_name=container_name,
#         blob_name=blob_name,
#         permission=AccountSasPermissions(read=True),
#         # how long the access is allowed before link access is revoked
#         expiry=datetime.utcnow() + timedelta(hours=1)
#     )
#     # generate the blob
#     url_with_sas = f"{url}?{sas_token}"
#     # return the url to access the blob
#     return url_with_sas
#     # Tryed on my system with an image it workes
#     # upload_file_path = "C:/Users/HP/Pictures/test.png"
#     # file = open(upload_file_path, 'rb')
#     # url_to_image_on_azure_blob = upload_image_and_generate_image_url(file_name='image.png', file=file)
#     # file.close()

#     #print(url_to_image_on_azure_blob)