import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

from intis import IntisClient, IntisError
from examples.conf import API_LOGIN, API_KEY, API_HOST


client = IntisClient(API_LOGIN, API_KEY, host=API_HOST)
try:
    hrl_response_list = client.make_hrl_request('79143453229')
    for hrl_response in hrl_response_list:
        print(vars(hrl_response))
except IntisError as e:
    print(e)