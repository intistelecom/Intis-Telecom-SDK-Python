
import six
import datetime


def datetime_convert(value):
    if isinstance(value, six.string_types) and value not in ['0000-00-00 00:00:00', '']:
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass

    return None


def date_convert(value):
    if isinstance(value, six.string_types) and value not in ['0000-00-00', '']:
        try:
            return datetime.datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            pass

    return None


def time_convert(value):
    try:
        return datetime.datetime.strptime(value, '%H:%M:%S').time()
    except ValueError:
        return None


class ModelBase(object):

    use_not_specified = True
    fields = ()

    def __init__(self, *args, **kwargs):
        for use_kwargs, fields in enumerate(self.fields):
            for i, field in enumerate(fields):

                if isinstance(field, str):
                    value = kwargs.pop(field, None) if bool(use_kwargs) else args[i]
                    setattr(self, field, value)

                elif isinstance(field, (list, tuple)):
                    value = kwargs.pop(field[0], None) if bool(use_kwargs) else args[i]
                    to_python = field[1]
                    try:
                        setattr(self, field[0], to_python(value))
                    except Exception as e:
                        setattr(self, field[0], None)

        if self.use_not_specified:
            for key, value in kwargs.items():
                setattr(self, key, value)


class Balance(ModelBase):
    """
    Class of getting balance

    Parameters
    -----------------------
        money: Amount of money
        currency: Name of currency
    """

    fields = (
        (),
        (('money', float), 'currency')
    )


class PhoneBase(ModelBase):
    """
    Class for getting data of phone number list

    Parameters
    -----------------------
        id: ID of phone list
        name: Name of phone list
        time_birth: Time for sending greetings
        day_before: The number of days to send greetings before
        local_time: Use local time of subscriber while SMS sending
        birth_sender: Time for sending greetings
        on_birth: Key that is responsible for sending greetings
        count: Number of pages in phone list
        pages: Key send/do not send birthday greetings
    """

    fields = (
        (('id', int),),
        ('name', ('time_birth', time_convert), ('day_before', int), ('local_time', int), 'birth_sender', 'birth_text', 'on_birth',
         ('count', int), 'pages')
    )


class PhoneBaseNumber(ModelBase):
    """
    Class of getting subscriber's data in the phone list

    Parameters
    -----------------------
        phone: Subscriber's phone number
        name: Subscriber's name
        last_name: Subscriber's middle name
        middle_name: Subscriber's last name
        date_birth: Subscriber's gender
        male: Subscriber's gender
        note1: Note 1
        note2: Note 2
        region: Subscriber's region
        operator: Subscriber's operator
    """

    fields = (
        ('phone',),
        ('name', 'last_name', 'middle_name', ('date_birth', date_convert), 'male', 'note1', 'note2', 'region', 'operator')
    )


class Sender(ModelBase):
    """
    Class for getting sender's status

    Parameters
    -----------------------
        sender: Sender's name
        state: Sender's status

    Using check status
    -----------------------
    if sender.state == sender.COMPLETED:
        pass
    """

    fields = (
        ('sender', 'state'),
    )

    COMPLETED = 'completed'
    ORDER = 'order'
    REJECTED = 'rejected'

    def is_completed(self):
        return self.state == self.COMPLETED

    def is_order(self):
        return self.state == self.ORDER

    def is_rejected(self):
        return self.state == self.REJECTED


class Message(ModelBase):
    """
    Class of getting response to SMS sending

    Parameters
    -----------------------
        phone: Phone number
        error: Text of the error while SMS sending
        id_sms: Message ID
        cost: Price of message
        count_sms: Number of message parts
    """

    fields = (
        ('phone',),
        ('error', ('id_sms', int), ('cost', float), ('count_sms', int))
    )


class MessageStatus(ModelBase):
    """
    Class for getting statuses of messages

    Parameters
    -----------------------
        id: Message ID
        status: string status of message
        time: datetime

    Using check status
    -----------------------
    if message_status.status == message_status.DELIVER:
        pass

    """

    fields = (
        ('id',),
        ('status', ('time', datetime_convert)),
    )

    DELIVER = 'deliver'
    EXPIRED = 'expired'
    NOT_DELIVER = 'not_deliver'
    PARTLY_DELIVER = 'partly_deliver'

    def is_delivered(self):
        return self.status == self.DELIVER


class InboxMessage(ModelBase):
    """
    Class for getting incoming message

    Parameters
    -----------------------
        id: Message ID
        date: Date of message receiving
        phone:
        sender: Sender's name
        prefix: Prefix of the incoming message
        text: Text of message
    """

    fields = (
        (('id', int),),
        (('date', datetime_convert), 'sender', 'phone', 'prefix', 'text'),
    )


class StopList(ModelBase):
    """
    Class for number for stop list

    Parameters
    -----------------------
        id: ID of stop list
        time_in: Time of adding to stop list
        description: Reason for adding to stop list
    """

    fields = (
        (('id', int),),
        (('time_in', datetime_convert), 'description')
    )


class Template(ModelBase):
    """
    Class for getting user's templates

    Parameters
    -----------------------
        id: ID of template
        name: Name of template
        template: Text of template
        up_time: Time of adding template
    """

    fields = (
        (('id', int),),
        ('name', 'template', ('up_time', datetime_convert))
    )


class DeliverStatistic(object):

    DELIVERED = 'deliver'
    EXPIRED = 'expired'

    def __init__(self, cost, parts, status):
        self.cost = float(cost)
        self.parts = int(parts)
        self.status = status

    def is_delivered(self):
        return self.status == self.DELIVERED

    def is_expired(self):
        return self.status == self.EXPIRED


class Statistic(ModelBase):
    """
    Class for getting daily statistics

    Parameters
    -----------------------
        date: Date for statistics output
        stats: Messages
    """

    fields = (
        (('date', date_convert), 'stats'),
    )

    def __init__(self, date, stats, **kwargs):
        super(Statistic, self).__init__(date, stats, **kwargs)
        self.stats = []
        for stat in stats:
            self.stats.append(DeliverStatistic(**stat))


class HLRResponse(ModelBase):
    """
    Class for getting HLR request

    Parameters
    -----------------------
        id: ID of number
        destination: Recipient
        stat: Status of subscriber
        IMSI: IMSI of subscriber
        err: Error message
        orn: The original name of the subscriber's operator
        pon: Prefix of operator if the phone number of the subscriber is ported
        ron: Operator in the subscriber's roaming
        mccmnc: MCC of subscriber
        rcn: Name of country in the subscriber's roaming
        ppm: Price for message
        onp: The original prefix of the subscriber's operator
        ocn: The original name of the subscriber's country
        ocp: The original code of the subscriber's country
        is_ported: Key that is responsible for identification of a ported number
        rnp: Prefix of operator in the subscriber's roaming
        rcp: Prefix of country in the subscriber's roaming
        is_roaming: Key that is responsible for identification a subscriber in roaming
        pnp: Prefix of operator if the phone number of the subscriber is ported
        pcn: Name of country if the phone number of the subscriber is ported
        pcp: Prefix of country if the phone number of the subscriber is ported
    """

    fields = (
        (),
        ('id', 'destination', 'stat', 'IMSI', 'err', 'orn', 'pon', 'ron', 'mccmnc', 'rcn', ('ppm', float), 'onp',
         'ocn', 'ocp', 'is_ported', 'rnp', 'rcp', 'is_roaming', 'pnp', 'pcn', 'pcp')
    )


class HLRStatistic(HLRResponse):
    """
    Class of statistics by HLR requests

    Parameters
    -----------------------
        phone: Phone number
        message_id: Message ID
        total_price: Final price
        request_id: Request ID
        request_time: Time of HLR request
    """

    fields = (
        ('phone',),
        ('message_id', ('total_price', float), 'request_id', 'request_time') + HLRResponse.fields[1]
    )


class Price(ModelBase):
    """
    Class for getting prices

    Parameters
    -----------------------
        id:
        network_name:
        country:
        price:
        currency:
    """

    fields = (
        (('id', int),),
        ('network_name', 'country', ('price', float), 'currency')
    )


class Operator(ModelBase):
    """
    Class for getting mobile operator info

    Parameters
    -----------------------
    """
    fields = (
        (),
        ('country', 'currency', 'mcc', 'mnc', 'operator', 'phone', 'ported', 'price', 'regionCode', 'timeZone')
    )
