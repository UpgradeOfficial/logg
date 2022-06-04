import json
from multiprocessing.connection import Client
import requests
import hmac
import hashlib
from django.conf import Settings, settings
from django.core.exceptions import ValidationError

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

    def generate_digest(self, data, secret=settings.PAYSTACK_PRIVATE_KEY):
        return hmac.new(
        secret.encode("utf-8"), msg=json.dumps(data).encode('utf-8'), digestmod=hashlib.sha512
    ).hexdigest()

    def webhook(self, request ):
        IP_whitelisting =["52.31.139.75", "52.49.173.169", "52.214.14.220"]
        
        webhook_data = request.data
        hash = self.generate_digest(webhook_data)
        if (request.headers['X-Forwarded-For'] in IP_whitelisting) == False:
            raise ValidationError(f"Ip not allowed {request.headers['X-Forwarded-For']}")
        if hash != request.headers["X-Paystack-Signature"]:
            raise ValidationError("MAC authentication failed")

        if webhook_data["event"] == "charge.success":
            pass

        return webhook_data
        
    def create_split_account(self, school_name, account_number,  settlement_bank):
        url = "subaccount/" #f"transactions/{payment_ref}/verify/"
        data = { 
            "business_name": school_name,
            "settlement_bank": settlement_bank,
            "account_number": account_number,
            "percentage_charge": Settings.PERCENTAGE_CHARGE
        }
        response = self.request(method="POST", path=url, payload=data)
        response_dict = response['data']
        return response_dict

    def get_all_banks(self, name_of_bank=None):
        url = "bank/" 
        response = self.request(method="GET", path=url)
        response_dict = response['data']
        if name_of_bank:
            for banks in response_dict:
                pass
        return  response_dict

    def resolve_bank_account(self, bank_code, account_number):
        url = f"bank/resolve?account_number={account_number}&bank_code={bank_code}" 
        response = self.request(method="GET", path=url)
        if response["status"] == True and response["message"] == "Account number resolved":
            response_dict = response['data']
        else:
            response_dict = {"message": "data not verified"}
        return response_dict