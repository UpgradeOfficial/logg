
# Create your views here.
import json
import os
from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from .serializers import ContactUsSerializer
from core.utils import send_mail



from django.conf import settings
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes
from .utils import render_to_pdf
from django.http import HttpResponse
from django.views import View




class Custom404(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        response_data = {
            "message": "Not found!",
            "status_code": 404,
            "result": None,
        }
        return Response(response_data, status=HTTP_404_NOT_FOUND)

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def put(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.get(*args, **kwargs)


def custom_500_handler(request, *args, **argv):
    return JsonResponse(
        {"status_code": 500, "message": "Internal Server Error!", "result": None},
        status=500,
    )

def redirect_to_swagger(request):
    ...
    return redirect('swagger-ui')


class PhoneCode(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Success.",
                examples=[
                    OpenApiExample(
                        name="example 1",
                        value=[{"name": "string", "phone_code": "string"}],
                    )
                ],
                response=[OpenApiTypes.STR],
            )
        },
    )
    def get(self, *args, **kwargs):
        data = json.load(open(os.path.join(settings.BASE_DIR , "data" , "json","country_phone_code.json")))
        return Response({"status_code": 200, "message": "Success.", "result": data})

class ContactUsView(APIView):
    '''
    THIS API IS USED TO SEND MESSAGE TO THE ADMIN AND IS
    ACCESSIBLE BY ANY ONE
    '''
    serializer_class = ContactUsSerializer()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        '''
        THIS API IS USED TO SEND MESSAGE TO THE ADMIN AND IS
        ACCESSIBLE BY ANY ONE. IT ACCESS VIA POST REQUEST AND THE EMAIL OF
        THE SENDER IS COLLECT FOR FEEDBACK PURPOSES
        '''
        serializer = ContactUsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subject = serializer.validated_data['subject']
        email = serializer.validated_data['email']
        text = serializer.validated_data['text']
        name = serializer.validated_data['name']      
        context = {
            'name':name,
            'text':text,
            'email': email
        }
        send_mail(subject=subject, to_email=settings.BACKEND_ADMIN_EMAIL, input_context=context, template_name='contact_us.html', cc_list=[], bcc_list=[])
        return Response(status=status.HTTP_200_OK, data={'message':"You message has been received and is been processed."})


        #Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):

		pdf = render_to_pdf('contact_us.html', context_dict={'name':"Increase", 'text':"this is it"})
		return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		
		pdf = render_to_pdf('contact_us.html', context_dict={'name':"Increase", 'text':"this is it"})

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Invoice_%s.pdf" %("12341231")
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response



def index(request):
	context = {}
	return render(request, 'app/index.html', context)