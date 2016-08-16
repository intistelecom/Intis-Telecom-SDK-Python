import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

from intis import IntisClient, IntisError
from examples.conf import API_LOGIN, API_KEY, API_HOST
client = IntisClient(API_LOGIN, API_KEY, host=API_HOST)
try:
    phone_bases = client.get_phone_bases()
    for phone_base in phone_bases:
        phone_base_numbers = client.get_phone_base_numbers(phone_base.id)
        for phone_base_number in phone_base_numbers:
            pprint(vars(phone_base_number))
except IntisError as e:
    print(e)
