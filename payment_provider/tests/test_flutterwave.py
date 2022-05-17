from django.urls import reverse
from django.test import TestCase
from unittest import mock

# Create your tests here.
verification_success = {
  "status": "success",
  "message": "Transaction fetched successfully",
  "data": {
    "id": 288200108,
    "tx_ref": "LiveCardTest",
    "flw_ref": "YemiDesola/FLW275407301",
    "device_fingerprint": "N/A",
    "amount": 100,
    "currency": "NGN",
    "charged_amount": 100,
    "app_fee": 1.4,
    "merchant_fee": 0,
    "processor_response": "Approved by Financial Institution",
    "auth_model": "PIN",
    "ip": "::ffff:10.5.179.3",
    "narration": "CARD Transaction ",
    "status": "successful",
    "payment_type": "card",
    "created_at": "2020-07-15T14:31:16.000Z",
    "account_id": 17321,
    "card": {
      "first_6digits": "232343",
      "last_4digits": "4567",
      "issuer": "FIRST CITY MONUMENT BANK PLC",
      "country": "NIGERIA NG",
      "type": "VERVE",
      "token": "flw-t1nf-4676a40c7ddf5f12scr432aa12d471973-k3n",
      "expiry": "02/23"
    },
    "meta": None,
    "amount_settled": 98.6,
    "customer": {
      "id": 216519823,
      "name": "Yemi Desola",
      "phone_number": "N/A",
      "email": "user@gmail.com",
      "created_at": "2020-07-15T14:31:15.000Z"
    }
  }

}

flutterwave_payment_data = {
  "status": "success",
  "message": "Hosted Link",
  "data": {
    "link": "https://api.flutterwave.com/v3/hosted/pay/f524c1196ffda5556341"
  }
}
class PaymentTest(TestCase):
    @mock.patch('payment_provider.flutterwave.FluterwaveProviver.request', return_value=flutterwave_payment_data)
    def test_payment(self, _mock_api):
        url = reverse("payment_provider:pay")
        data = {
            "email": "odeyemiincrease@yahoo.com",
            "amount": 10,
            "provider": "F"
         }
        res = self.client.post(url , data = data)
        response_data = res.json()
        self.assertTrue('authorization_url' in response_data)

    @mock.patch('payment_provider.flutterwave.FluterwaveProviver.request', return_value=verification_success)
    def test_verify_payment(self, _mock_api):
        url = reverse("payment_provider:verify_payment")
        data = {
            "tx_ref": "3360619", #&transaction_id=3360619
            "provider": "F"
         }
        res = self.client.post(url , data = data)
        response_data = res.json()
        self.assertTrue("amount" in response_data)
