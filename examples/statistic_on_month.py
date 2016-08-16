import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

from intis import IntisClient, IntisError
from examples.conf import API_LOGIN, API_KEY, API_HOST


client = IntisClient(API_LOGIN, API_KEY, host=API_HOST)
try:
    statistic_list = client.get_statistic_on_month(2014, 12)
    for statistic in statistic_list:
        print(vars(statistic))
except IntisError as e:
    print(e)