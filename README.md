python-intis
======
A Python 2/3 client for the Intis CMS APIs http://www.sms16.ru/

Installation
-----
pip install python-intis

Requires
-----
  * six

##Examples
```python
from intis import IntisClient, IntisApiError
API_LOGIN = 'LOGIN'
API_KEY = 'KEY'
client = IntisClient(API_LOGIN, API_KEY)
try:
    balance = client.get_balance()
    balance.money
except IntisApiError as e:
    print(e)
```