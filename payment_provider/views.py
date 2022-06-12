from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from payment_provider import flutterwave, paystack
from .serializers import PaymentSerializer, PaymentVerificationSerializer
from .gateway import Gateway
# Create your views here.
class PaymentView(CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        data = serializer.validated_data
        provider = Gateway().get_payment_gateway(data['provider'])
        email = data['email']
        amount = data['amount']
        auth_url, id=provider.pay_amount(email=email, amount=amount)
        serializer.context['authorization_url'] = auth_url 

class PaymentVerificationView(APIView):
    serializer_class = PaymentVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        provider = Gateway().get_payment_gateway(data['provider'])
        result=provider.verify_payment(data['tx_ref'])
        
        return Response(status=status.HTTP_200_OK, data=result)

class PaystackWebhookView(APIView):
    permission_classes = [AllowAny]

    def  post(self, request, *args, **kwargs):
        data = paystack.PaystackProvider().webhook(request)
        return Response(status=status.HTTP_200_OK)
        
class FlutterwaveWebhookView(APIView):
    permission_classes = [AllowAny]

    def  post(self, request, *args, **kwargs):
        
        data = flutterwave.FluterwaveProviver().webhook(request)
        return Response(status=status.HTTP_200_OK)

class BankCodeNameView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        provider_query_string = self.request.query_params.get('provider')
        provider = Gateway().get_payment_gateway(provider=provider_query_string)
        data=provider.get_all_banks()
        return Response(status=status.HTTP_200_OK, data=data)

class VerifyBankAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self,  *args, **kwargs):
        data = self.request.data
        provider = data['provider']
        bank_code = data['bank_code']
        account_number = data['account_number']
        provider = Gateway().get_payment_gateway(provider=provider)
        data=provider.resolve_bank_account(bank_code=bank_code, account_number=account_number)
        return Response(status=status.HTTP_200_OK, data=data)

class CreateSubAccountView(APIView):
    permission_classes = [AllowAny]

    def post(self,  *args, **kwargs):
        data = self.request.data
        provider = data['provider']
        bank_code = data['bank_code']
        account_number = data['account_number']
        provider = Gateway().get_payment_gateway(provider=provider)
        data=provider.create_split_account(bank_code=bank_code, account_number=account_number)
        return Response(status=status.HTTP_200_OK, data=data)



        