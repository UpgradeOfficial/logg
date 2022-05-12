from django.urls import reverse
from django.test import TestCase
from unittest import mock

# Create your tests here.
verification_success = {
  
}

flutterwave_payment_data = {
 
}
class PaymentTest(TestCase):
    # @mock.patch('payment_provider.flutterwave.FluterwaveProviver.request', return_value=flutterwave_payment_data)
    # def test_payment(self):
    #     url = reverse("payment_provider:pay")
    #     data = {
    #         "email": "odeyemiincrease@yahoo.com",
    #         "amount": 10,
    #         "provider": "T"
    #      }
    #     res = self.client.post(url , data = data)
    #     response_data = res.json()
    #     print(response_data)
    #     self.assertTrue('authorization_url' in response_data)

    @mock.patch('payment_provider.flutterwave.FluterwaveProviver.request', return_value=verification_success)
    def test_verify_payment(self, _mock_api):
        url = reverse("payment_provider:verify_payment")
        data = {
            "tx_ref": "i6tafv4lmh", #&transaction_id=3360619
            "provider": "T"
         }
        res = self.client.post(url , data = data)
        response_data = res.json()
        print(response_data)
        self.assertTrue("amount" in response_data)
