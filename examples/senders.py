
from intis import IntisClient, IntisError

from examples.conf import API_LOGIN, API_KEY, API_HOST


client = IntisClient(API_LOGIN, API_KEY, host=API_HOST)
try:
    senders = client.get_senders()
    for sender in senders:
        print(vars(sender))
except IntisError as e:
    print(e)