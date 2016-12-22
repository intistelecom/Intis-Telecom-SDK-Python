Intis-Telecom-SDK-Python
========================

The Intis telecom gateway lets you send SMS messages worldwide via its API. This program sends HTTP(s) requests and receives information as a response in JSON and/or XML. The main functions of our API include:

* sending SMS messages (including scheduling options);
* receiving status reports about messages that have been sent previously;
* requesting lists of authorised sender names;
* requesting lists of incoming SMS messages;
* requesting current balance status;
* requesting lists of databases;
* requesting lists of numbers within particular contact list;
* searching for a particular number in a stop list;
* requesting lists of templates;
* adding new templates;
* requesting monthly statistics;
* making HLR request;
* HLR запрос
* receiving HLR request statistics;
* requesting an operator’s name by phone number;

To begin using our API please [apply](https://go.intistele.com/external/client/register/) for your account at our website where you can get your login and API key.

Install
---------------------------
```bash
pip install intis
```

Usage
---------------------------

class IntisClient - The main class for SMS sending and getting API information

There are three mandatory parameters that you have to provide the constructor in order to initialize. They are:
* API_LOGIN - user login
* API_KEY - user API key

```python
from intis import IntisClient, IntisApiError

API_LOGIN = 'LOGIN'
API_KEY = 'KEY'

client = IntisClient(API_LOGIN, API_KEY)
```

This class includes the following methods:
--------------------------------

Use the `get_balance()` method to request your balance status
```python
try:
    balance = client.get_balance()
    balance.money
except IntisApiError as e:
    print(e)
```
