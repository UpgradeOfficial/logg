import requests
from django.conf import settings

from core.utils import random_with_N_digits
from .gateway import Gateway, GatewayException

PAYSTACK_BASE_URL = "https://api.paystack.co/"

class PaystackProvider(Gateway):

    def request(self, method, path, payload={}, params={}):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.PAYSTACK_PRIVATE_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.request(method, PAYSTACK_BASE_URL + path, json=payload, params=params, headers=headers)
        if response.status_code != 200:
            raise Exception()
        response_dict = response.json()
        if response_dict['status'] != True:
            raise Exception()
        return response_dict

    def pay_amount(self, amount, email):
        url = 'transaction/initialize'
        data = { 
            "email": email,
             "amount": str( amount*100),
             "callback_url": f'{settings.CARD_PAYMENT_SUCCESS_URL}?&method=paystack' 
        }
        response = self.request(method="POST", path=url, payload=data)
        data = response
       

        redirect_url = data['data']['authorization_url']
        id = data['data']['reference']
        return redirect_url, id

    def verify_payment(self, refernce):
        # reference=3360619
        # it is always appended to the redirect url
        url = f"transaction/verify/{refernce}" #f"transactions/{payment_ref}/verify/"
        data = self.request(method="GET",path=url)
        data = data['data']
        if data['status'] != 'success':
            raise GatewayException("Payment not found")
        # amount_data = data['amount']
        # if int(amount_data/100) != payment_amount :
        #     logging.error(f'amount={payment_amount} requested, but {amount_data} found in payment')
        #     raise GatewayException("Invalid payment amount")
        return data