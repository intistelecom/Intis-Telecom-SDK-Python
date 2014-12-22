
from intis import IntisClient

from examples.conf import API_LOGIN, API_KEY, API_HOST


client = IntisClient(API_LOGIN, API_KEY, host=API_HOST)
messages = client.message_send('79141231212', 'SMS4TEST', 'hello')
for message in messages:
    print(vars(message))