import logging
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from core.utils import random_with_N_digits
from .gateway import Gateway, GatewayException
import requests

FLUTTERWAVE_BASE_URL = 'https://api.flutterwave.com/v3/'

class FluterwaveProviver(Gateway):

    def request(self, method, path, payload={}, params={}):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.FLUTTERWAVE_PRIVATE_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.request(method, FLUTTERWAVE_BASE_URL + path, json=payload, params=params, headers=headers)
        if response.status_code != 200:
            raise Exception()
        response_dict = response.json()
        if response_dict['status'] != 'success':
            raise Exception()
        return response_dict

    def pay_amount(self, amount, email):
        url = 'payments/'
        transaction_reference = random_with_N_digits(10)
        data = {
            'tx_ref': str(transaction_reference),#"hooli-tx-1920bbtytty",
            'amount': amount,
            'currency': "USD",
            'redirect_url': f'{settings.CARD_PAYMENT_SUCCESS_URL}?method=flutterwave',
            'meta': {
                'consumer_id': 23,
                'consumer_mac': "92a3-912ba-1192a"
            },
            'customer': {
                'email': email,
                'phonenumber': "07068448786",
                'name': "Odeyemi Increase"
            },
             'customizations': {
                 'title': "Logg Inc",
                 'logo': "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
             }
        }
        response = self.request(method="POST", path=url, payload=data)
        data = response
        redirect_url = data['data']['link']
        id = transaction_reference
        return redirect_url, id

    def verify_payment(self, transaction_id):
        # transaction_id=3360619
        # it is always appended to the redirect url
        url = f"transactions/{transaction_id}/verify/" #f"transactions/{payment_ref}/verify/"
        data = self.request(method="GET", path=url)
        data = data['data']
        if data['status'] != 'successful':
            raise GatewayException("Payment not found")
        return data

    def webhook(self, request):
        if request.headers.get('Verif-Hash') != settings.FLUTTERWAVE_SECRET_HASH:
            raise AuthenticationFailed()
        return request.data