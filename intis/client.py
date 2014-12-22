from __future__ import unicode_literals, print_function

import json
import hashlib

try:
    import urllib.request as urllib_request
    import urllib.error as urllib_error
    from urllib.parse import urlencode
except ImportError:
    import urllib2 as urllib_request
    import urllib2 as urllib_error
    from urllib import urlencode


from intis.exceptions import IntisApiError, IntisHTTPError, ERROR_EMPTY_RESPONSE_CODE
from intis.utils import wrap_result
from intis.models import *

EMPTY_VALUES = [None, '', {}, [], 'null']
DEFAULT_HOST = 'https://new.sms16.ru/get/'


class IntisBaseClient(object):
    """
    The main class for working with API
    """

    def http_response(self, url):
        """
        Getting data response by url
        :param url: url
        :return: string
        """
        try:
            handle = urllib_request.urlopen('%s%s' % (self.host, url))
        except urllib_error.HTTPError as e:
            raise IntisHTTPError(e)

        response = handle.read()
        response = response.decode('utf-8', errors='ignore')

        return response

    @property
    def timestamp(self):
        """
        Getting time in UNIX format from the file timestamp.php in API
        :return: string
        """
        return self.http_response('timestamp.php')

    def get_signature(self, params):
        """
        Getting signatures by incoming parameters
        :param params: dict
        :return: string
        """
        sig = '%s%s' % (''.join([str(params[key]) for key in sorted(params)]), self.key)
        return hashlib.md5(sig.encode('utf-8')).hexdigest()

    def prepare_params(self, extra_params={}):
        """
        Prepare all parameters for API.
        :param extra: extra parameters
        :return: parameters
        """
        params = {
            'login': self.login,
            'timestamp': self.timestamp,
            'return': 'json'
        }
        params.update(extra_params)
        params['signature'] = self.get_signature(params)
        return params

    def get_result(self, script_name, params={}):
        """
        Getting data from API.
        :param script_name: php script name
        :param params: api parameters
        :return:
        """
        params = self.prepare_params(params)

        url = '%s.php?%s' % (script_name, urlencode(params))
        response = self.http_response(url)
        print('Debug: %s\n' % response)

        try:
            result = json.loads(response)
        except TypeError as e:
            raise IntisApiError(0)

        if result in EMPTY_VALUES:
            raise IntisApiError(ERROR_EMPTY_RESPONSE_CODE)

        if 'error' in result:
            raise IntisApiError(result['error'])

        return result


class IntisClient(IntisBaseClient):

    def __init__(self, login, key, host=DEFAULT_HOST, raise_empty=False):
        """
        The main class for SMS sending and getting API information
        :param login: user's login
        :param key: user's API key
        :param host: API address
        :param raise_empty: raise IntisException if response is empty
        """
        self.login = login
        self.key = key
        self.host = host
        self.raise_empty = raise_empty

    @wrap_result(Balance)
    def get_balance(self):
        """
        Getting user's balance
        :return Balance
        """
        return self.get_result('balance')

    @wrap_result(Sender, multiple=True, key_are_value=True)
    def get_senders(self):
        """
        Getting all the user's sender's names
        :return list of Sender
        """
        return self.get_result('senders')

    @wrap_result(PhoneBase, multiple=True)
    def get_phone_bases(self):
        """
        Getting all the user's phone number lists
        :return list of PhoneBase
        """
        return self.get_result('base')

    @wrap_result(PhoneBaseNumber, multiple=True)
    def get_phone_base_numbers(self, base_id, page=1):
        """
        Getting subscribers of phone number list
        :param base_id: ID of phone number list
        :param page: Page of phone number list
        :return list of PhoneBaseNumber
        """
        params = {
            'base': base_id,
            'page': page
        }
        return self.get_result('phone', params)

    @wrap_result(Message, multiple=True)
    def message_send(self, phone, sender, text):
        """
        :param phone: phone number(s)
        :param sender: sender's name
        :param text: sms text
        :return: Message
        """
        if isinstance(phone, (list, tuple)):
            phone = ','.join(phone)

        return self.get_result('send', {
            'phone': phone,
            'sender': sender,
            'text': text
        })

    @wrap_result(MessageStatus, multiple=True)
    def get_message_status(self, message_id):
        """
        Getting message status
        :param message_id: Message ID
        :return list of Sender
        """
        if isinstance(message_id, (list, tuple)):
            message_id = ','.join(message_id)

        return self.get_result('status', {'state': message_id})

    @wrap_result(StopList)
    def find_in_stop_list(self, phone):
        """
        Finding phone number for stop list
        :param phone: phone number
        :return: StopList
        """
        return self.get_result('find_on_stop', {'phone': phone})

    def add_to_stop_list(self, phone):
        """
        Adding number to stop list
        :param phone:
        :return: id
        """
        result = self.get_result('add2stop', {'phone': phone})
        return result['id']

    @wrap_result(Template, multiple=True)
    def get_templates(self):
        """
        Getting user's templates
        :return: list of Template
        """
        return self.get_result('template')

    def add_template(self, name, text):
        """
        Adding user's template
        :param name: template name
        :param text: template text
        :return: id
        """
        result = self.get_result('add_template', {'name': name, 'text': text})
        return result['id']

    @wrap_result(Statistic, multiple=True)
    def get_statistic_on_month(self, year, month):
        """
        Getting statistics for the certain month
        :param year: Year
        :param month: Month
        :return: list of Statistic
        """
        return self.get_result('stat_by_month', {'month': '%s-%s' % (str(year), str(month))})

    def get_network_by_phone(self, phone):
        """
        Getting the operator of subscriber's phone number
        :param phone: phone number
        :return: operator name
        """
        result = self.get_result('operator', {'phone': phone})

        return result.get('operator', None) if isinstance(result, dict) else None

    @wrap_result(HLRStatistic, multiple=True)
    def get_hlr_statistic(self, date_from, date_to):
        """
        Getting statuses of HLR request
        :param date_from: Date from (YYYY-MM-DD)
        :param date_to: Date to (YYYY-MM-DD)
        :return: list of HLRStatistic
        """
        return self.get_result('hlr_stat', {'from': date_from, 'to': date_to})

    @wrap_result(HLRResponse, multiple=True)
    def make_hrl_request(self, phone):
        """
        Sending HLR request for number
        :param phone: phone numbers
        :return: list of HLRResponse
        """
        if isinstance(phone, (list, tuple)):
            phone = ','.join(phone)

        return self.get_result('hlr', {'phone': phone})

    @wrap_result(InboxMessage, multiple=True)
    def get_inbox_messages(self, date):
        """
        Getting incoming messages of certain date
        :param date: date (YYYY-MM-DD)
        :return: list of MessageInbox
        """
        return self.get_result('incoming', {'date': date})