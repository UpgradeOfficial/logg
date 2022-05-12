from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
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




        