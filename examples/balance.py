
from intis import IntisClient, IntisError

from examples.conf import API_LOGIN, API_KEY, API_HOST


client = IntisClient(API_LOGIN, API_KEY, host=API_HOST)
try:
    balance = client.get_balance()
    print(vars(balance))
except IntisError as e:
    print(e)