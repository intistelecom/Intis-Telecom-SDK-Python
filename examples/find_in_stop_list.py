
from intis import IntisClient, IntisError

from examples.conf import API_LOGIN, API_KEY, API_HOST


client = IntisClient(API_LOGIN, API_KEY, host=API_HOST)
try:
    stop_list = client.find_in_stop_list('79141231212')
    print(vars(stop_list))
except IntisError as e:
    print(e)