
from intis import IntisClient, IntisError

from examples.conf import API_LOGIN, API_KEY, API_HOST


client = IntisClient(API_LOGIN, API_KEY, host=API_HOST)
try:
    id = client.add_to_stop_list('79141231212')
    print(id)
except IntisError as e:
    print(e)