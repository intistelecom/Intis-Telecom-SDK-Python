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
    balanve.currency
except IntisApiError as e:
    print(e)
```


To get a list of all the contact databases you have use the function `get_phone_bases()`
```python
for base in client.get_phone_bases():
    base.id
    base.name
    base.count
    base.pages
```

Our gateway supports the option of having unlimited sender’s names. To see a list of all senders’ names use the method `get_senders()`
```python
for sender in client.get_senders():
    sender.sender
    sender.state
```

To send a message (to one or several recipients), use the function `message_send(phone, sender, text)`,
where `phone` - is a set of numbers you send your messages to,
`sender` is a sender’s name and `text` stands for the content of the message.
```python
sender = client.get_senders()[0]
messages = client.message_send(settings.phone, sender.sender, 'Test message')
for message in messages:
    status = self.client.get_message_status(message.id_sms)[0]
    if status.is_delivered():
        status.time
```

To get a list of incoming messages please use the function `get_inbox_messages(date)`, where `date` stands for a particular day in YYYY-mm-dd format.
```python
for message in client.get_inbox_messages(date_from):
    message.id
    message.date
    message.sender
    message.phone
    message.prefix
    message.text
```
