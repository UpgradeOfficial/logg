import json
from multiprocessing.connection import Client
import requests
import hmac
import hashlib
from django.conf import Settings, settings
from django.core.exceptions import ValidationError

from core.utils import random_with_N_digits
from .gateway import Gateway, GatewayException
from rest_framework.exceptions import ValidationError

PAYSTACK_BASE_URL = "https://api.paystack.co/"

class PaystackProvider(Gateway):

    def request(self, method, path, payload={}, params={}):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.PAYSTACK_PRIVATE_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.request(method, PAYSTACK_BASE_URL + path, json=payload, params=params, headers=headers)
        response_dict = response.json()
        if response.status_code != 200:
            raise ValidationError(response_dict.get('message') or 'Something went wrong. Try again or contact admin')
        
        if response_dict['status'] != True:
            raise ValidationError(response_dict.get('message') or 'Something went wrong. Try again or contact admin')
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
        
    

    def get_all_banks(self, name_of_bank=None):
        url = "bank/" 
        response = self.request(method="GET", path=url)
        response_dict = response['data']
        if name_of_bank:
            for banks in response_dict:
                pass
        return  response_dict

    def resolve_bank_account(self, bank_code, account_number):
        url = f"bank/resolve/"#?account_number={account_number}&bank_code={bank_code}" 
        params={
               "account_number":account_number,
               "bank_code":bank_code
        }
        response = self.request(method="GET", path=url, params=params)
        if response["status"] == True and response["message"] == "Account number resolved":
            response_dict = response['data']
        else:
            response_dict = {"message": "data not verified"}
        return response_dict

    def create_split_account(self, bank_code, account_number):
        print('yes')
        account = self.resolve_bank_account(bank_code=bank_code, account_number=account_number)
        print(account)
        url = "subaccount/" 
        print(settings.PERCENTAGE_CHARGE)
        data = { 
            "business_name": account.get('account_name'),
            "bank_code":  bank_code,
            "account_number": account.get("account_number"),
            "percentage_charge": settings.PERCENTAGE_CHARGE
        }
        response = self.request(method="POST", path=url, payload=data)

        print(response)

        #response_dict = response.json()
        #print(response_dict)
        return response


    # def resolve_bank_account_details(self, bank_code, account_number, account_name, account_type):
    #     url = f"bank/validate/"#?account_number={account_number}&bank_code={bank_code}" 
    #     print(url)
    #     data={ 
    #         "bank_code": "632005",
    #         "country_code": "ZA",
    #         "account_number": "0123456789",
    #         "account_name": "Ann Bron",
    #         "account_type": "personal",# [ personal, business ]
    #         "document_type": "identityNumber",#[ "identityNumber","passportNumber", "businessRegistrationNumber" ]
    #         "document_number": "1234567890123"
    #     }
    #     response = self.request(method="POST", path=url, data=data)
    #     if response["status"] == True and response["message"] == "Account number resolved":
    #         response_dict = response['data']
    #     else:
    #         response_dict = {"message": "data not verified"}
    #     return response_dict

  