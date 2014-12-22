
from intis import IntisClient, IntisError

from examples.conf import API_LOGIN, API_KEY, API_HOST


client = IntisClient(API_LOGIN, API_KEY, host=API_HOST)
try:
    network = client.get_network_by_phone('79090099090')
    print(network)
except IntisError as e:
    print(e)