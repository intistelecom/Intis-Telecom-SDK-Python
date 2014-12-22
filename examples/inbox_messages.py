
from intis import IntisClient, IntisError

from examples.conf import API_LOGIN, API_KEY, API_HOST


client = IntisClient(API_LOGIN, API_KEY, host=API_HOST)
try:
    inbox_messages = client.get_inbox_messages('2014-11-25')
    for inbox_message in inbox_messages:
        print(vars(inbox_message))
except IntisError as e:
    print(e)