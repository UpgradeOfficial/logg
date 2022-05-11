from google.auth.transport import requests
from google.oauth2 import id_token

class Google:

    @staticmethod
    def validate(auth_token):
        try:
            idInfo = id_token.verify_oauth2_token(auth_token, requests.Request())
            if "accounts.google.com" in idInfo["iss"]:
                return idInfo
        except:
            return "the token is either expired or is invalid"