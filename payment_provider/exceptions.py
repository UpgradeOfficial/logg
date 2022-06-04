from rest_framework.exceptions import APIException

class WrongData(APIException):
    status_code = 503
    default_detail = 'Wrong Data. Check your data'
    default_code = 'Wrong Data'