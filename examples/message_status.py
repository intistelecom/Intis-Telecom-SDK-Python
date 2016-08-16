import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

from intis import IntisClient, IntisError
from examples.conf import API_LOGIN, API_KEY, API_HOST


client = IntisClient(API_LOGIN, API_KEY, host=API_HOST)
try:
    message_status_list = client.get_message_status('4192072123106546180001')
    for message_status in message_status_list:
        print(vars(message_status))
except IntisError as e:
    print(e)
