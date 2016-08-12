
ERROR_CODES = {
    0: 'Service is disabled',
    1: 'Signature is not specified',
    2: 'Login is not specified',
    3: 'Text is not specified',
    4: 'Phone number is not specified',
    5: 'Sender is not specified',
    6: 'Incorrect signature',
    7: 'Incorrect login',
    8: 'Incorrect sender"s name',
    9: 'Unregistered sender"s name',
    10: 'Sender"s name is not approved',
    11: 'There are forbidden words in the text',
    12: 'SMS sending error',
    13: 'Phone number is in stop-list. SMS sending to this number is blocked',
    14: 'There are more than 50 numbers in the request',
    15: 'List is not specified',
    16: 'Invalid number',
    17: 'SMS ID are not specified',
    18: 'Status is not recieved',
    19: 'Empty response',
    20: 'This number is already taken',
    21: 'No name',
    22: 'This template is already created',
    23: 'Month is not specified (format: YYYY-MM)',
    24: 'Timestamp is not specified',
    25: 'Error in access to list',
    26: 'There are no numbers in the list',
    27: 'There are no valid numbers',
    28: 'Initial date is not specified',
    29: 'Final date is not specified',
    30: 'Date is not valid (format: YYYY-MM-DD)',
}

ERROR_EMPTY_RESPONSE_CODE = 19


class IntisError(Exception):
    pass


class IntisApiError(IntisError):
    """
    Base Exception thrown when there is a general error interacting with the API.
    """

    not_found_code = 'Error code "{0}" not found'

    def __init__(self, code):
        try:
            message = ERROR_CODES[code]
        except KeyError:
            message = self.not_found_code.format(code)
        self.code = code

        super(IntisApiError, self).__init__(message)

    def is_empty_response(self):
        return True if self.code == ERROR_EMPTY_RESPONSE_CODE else False


class IntisHTTPError(IntisError):
    """
    Exception thrown when there is an HTTP error interacting with sms16.ru.
    """

    def __init__(self, e, params={}):
        self.e = e
        self.params = params
        super(IntisHTTPError, self).__init__(str(self))

    def __str__(self):
        return (
            'Intis Http Error %s: %s' % (self.e.code, self.e.message)
        )
