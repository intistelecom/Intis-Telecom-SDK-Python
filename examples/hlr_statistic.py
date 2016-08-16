import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))

from intis import IntisClient, IntisError
from examples.conf import API_LOGIN, API_KEY, API_HOST


client = IntisClient(API_LOGIN, API_KEY, host=API_HOST)
try:
    hrl_statistics = client.get_hlr_statistic('2013-12-01', '2014-12-22')
    for hrl_statistic in hrl_statistics:
        print(vars(hrl_statistic))
except IntisError as e:
    print(e)