import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

from intis import IntisClient, IntisError
from examples.conf import API_LOGIN, API_KEY, API_HOST


client = IntisClient(API_LOGIN, API_KEY, host=API_HOST)
try:
    template_id = client.add_template('TEMPLATE_NAME', 'Some template text')
    print(template_id)
except IntisError as e:
    print(e)
