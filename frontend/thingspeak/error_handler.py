'''
Error codes may be found here:
https://www.mathworks.com/help/thingspeak/error-codes.html
'''


class Error:
    status = str
    error_code = str
    message = str
    details = str

    def __init__(self, error_json):
        self.status = error_json['status']
        error = error_json['error']
        self.error_code = error['error_code']
        self.message = error['message']
        self.details = error['details']


def get_error(response_json):
    if isinstance(response_json, dict) and response_json.get('error'):
        return Error(response_json)
    else:
        return None
