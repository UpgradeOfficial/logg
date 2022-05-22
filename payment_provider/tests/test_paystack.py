
import unittest
from unittest.mock import Mock
from django.urls import reverse
from django.test import RequestFactory, Client, TestCase
from rest_framework.test import APIClient
from unittest import mock

from payment_provider.paystack import PaystackProvider
from ..views import PaystackWebhookView
from hmac import new 

# Create your tests here.
paystack_verification_success = {
  "status": True,
  "message": "Verification successful",
  "data": {
    "amount": 27000,
    "currency": "NGN",
    "transaction_date": "2016-10-01T11:03:09.000Z",
    "status": "success",
    "reference": "DG4uishudoq90LD",
    "domain": "test",
    "metadata": 0,
    "gateway_response": "Successful",
    "message": None,
    "channel": "card",
    "ip_address": "41.1.25.1",
    "log": {
      "time_spent": 9,
      "attempts": 1,
      "authentication": None,
      "errors": 0,
      "success": True,
      "mobile": False,
      "input": [],
      "channel": None,
      "history": [{
        "type": "input",
        "message": "Filled these fields: card number, card expiry, card cvv",
        "time": 7
        },
        {
          "type": "action",
          "message": "Attempted to pay",
          "time": 7
        },
        {
          "type": "success",
          "message": "Successfully paid",
          "time": 8
        },
        {
          "type": "close",
          "message": "Page closed",
          "time": 9
        }
      ]
    },
    "fees": None,
    "authorization": {
      "authorization_code": "AUTH_8dfhjjdt",
      "card_type": "visa",
      "last4": "1381",
      "exp_month": "08",
      "exp_year": "2018",
      "bin": "412345",
      "bank": "TEST BANK",
      "channel": "card",
      "signature": "SIG_idyuhgd87dUYSHO92D",
      "reusable": True,
      "country_code": "NG",
      "account_name": "BoJack Horseman"
    },
    "customer": {
      "id": 84312,
      "customer_code": "CUS_hdhye17yj8qd2tx",
      "first_name": "BoJack",
      "last_name": "Horseman",
      "email": "bojack@horseman.com"
    },
    "plan": "PLN_0as2m9n02cl0kp6",
    "requested_amount": 1500000
  }
}

paystack_payment_data = {
  "status": True,
  "message": "Authorization URL created",
  "data": {
    "authorization_url": "https://checkout.paystack.com/0peioxfhpn",
    "access_code": "0peioxfhpn",
    "reference": "7PVGX8MEk85tgeEpVDtD"
  }
}

paystack_webhook_transaction_success_data = {  
  "event":"charge.success",
  "data": {  
    "id":302961,
    "domain":"live",
    "status":"success",
    "reference":"qTPrJoy9Bx",
    "amount":10000,
    "message":None,
    "gateway_response":"Approved by Financial Institution",
    "paid_at":"2016-09-30T21:10:19.000Z",
    "created_at":"2016-09-30T21:09:56.000Z",
    "channel":"card",
    "currency":"NGN",
    "ip_address":"41.242.49.37",
    "metadata":0,
    "log":{  
      "time_spent":16,
      "attempts":1,
      "authentication":"pin",
      "errors":0,
      "success":False,
      "mobile":False,
      "input":[],
      "channel":None,
      "history":[  
        {  
          "type":"input",
          "message":"Filled these fields: card number, card expiry, card cvv",
          "time":15
        },
        {  
          "type":"action",
          "message":"Attempted to pay",
          "time":15
        },
        {  
          "type":"auth",
          "message":"Authentication Required: pin",
          "time":16
        }
      ]
    },
    "fees":None,
    "customer":{  
      "id":68324,
      "first_name":"BoJack",
      "last_name":"Horseman",
      "email":"bojack@horseman.com",
      "customer_code":"CUS_qo38as2hpsgk2r0",
      "phone":None,
      "metadata":None,
      "risk_action":"default"
    },
    "authorization":{  
      "authorization_code":"AUTH_f5rnfq9p",
      "bin":"539999",
      "last4":"8877",
      "exp_month":"08",
      "exp_year":"2020",
      "card_type":"mastercard DEBIT",
      "bank":"Guaranty Trust Bank",
      "country_code":"NG",
      "brand":"mastercard",
      "account_name": "BoJack Horseman"
    },
    "plan":{}
  } 
}
class PaymentTest(TestCase):
    @mock.patch('payment_provider.paystack.PaystackProvider.request', return_value=paystack_payment_data)
    def test_payment(self, _mock_api):
        url = reverse("payment_provider:pay")
        data = {
            "email": "odeyemiincrease@yahoo.com",
            "amount": 10,
            "provider": "T"
         }
        res = self.client.post(url , data = data)
        response_data = res.json()
        self.assertTrue('authorization_url' in response_data)

    @mock.patch('payment_provider.paystack.PaystackProvider.request', return_value=paystack_verification_success)
    def test_verify_payment(self, _mock_api):
        url = reverse("payment_provider:verify_payment")
        data = {
            "tx_ref": "i6tafv4lmh", #&transaction_id=3360619
            "provider": "T"
         }
        res = self.client.post(url , data = data)
        response_data = res.json()
        self.assertTrue("amount" in response_data)

  
    def test_webhook(self):
        request = Mock(headers={ 
          'X-Forwarded-For':"52.31.139.75",
            'X-Paystack-Signature': PaystackProvider().generate_digest(paystack_webhook_transaction_success_data),
        }, data=paystack_webhook_transaction_success_data, body=paystack_webhook_transaction_success_data)
        res=PaystackProvider().webhook(request)
        self.assertEqual(res["event"],"charge.success")
        # self.assertTrue(True)
        
        
        
