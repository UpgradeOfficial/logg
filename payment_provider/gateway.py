from rest_framework.exceptions import ValidationError
from .models import PaymantProvider


class GatewayException(ValidationError):
    pass

class Gateway:

    def get_provider_type(self):
        raise NotImplemented

    @staticmethod
    def get_payment_gateway(provider):

        from .flutterwave import FluterwaveProviver
        from .paystack import PaystackProvider
        providers_dict = {
            PaymantProvider.FLUTTERWAVE: FluterwaveProviver(),
            PaymantProvider.PAYSTACK: PaystackProvider()
        }
        provider = providers_dict[provider]
        return provider

    