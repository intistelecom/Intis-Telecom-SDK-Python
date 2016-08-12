
import unittest

from intis import IntisClient, IntisApiError, models


class IntisTest(unittest.TestCase):

    def setUp(self):
        self.client = IntisClient('LOGIN', 'API_KEY', debug=True)

    def test_timestamp(self):
        self.assertRegex(self.client.timestamp, '^\d{10}$')

    def test_balance(self):
        balance = self.client.get_balance()
        self.assertIsInstance(balance, models.Balance)
        self.assertIsInstance(balance.money, float)
        self.assertIsInstance(balance.currency, str)

    def test_bases(self):
        for base in self.client.get_phone_bases():
            self.assertIsInstance(base, models.PhoneBase)
            self.assertIsInstance(base.id, int)

    def test_senders(self):
        for sender in self.client.get_senders():
            self.assertIsInstance(sender, models.Sender)

    def test_phones(self):
        bases = self.client.get_phone_bases()
        for base in bases:
            self.assertIsInstance(base, models.PhoneBase)
            phone_numbers = self.client.get_phone_base_numbers(base.id)
            for phone_number in phone_numbers:
                self.assertIsInstance(phone_number, models.PhoneBaseNumber)

    def test_message_send(self):
        sender = self.client.get_senders()[0]
        messages = self.client.message_send('+79000000000', sender.sender, 'Hello')
        for message in messages:
            self.assertIsInstance(message, models.Message)
            statuses = self.client.get_message_status(message.id_sms)
            for status in statuses:
                self.assertIsInstance(status, models.MessageStatus)

    def test_stop_list(self):
        phone = '79000000000'
        try:
            id = self.client.add_to_stop_list(phone)
            self.assertIsNotNone(id)
        except IntisApiError:
            pass

        find_stop_list = self.client.find_in_stop_list(phone)
        self.assertIsNotNone(find_stop_list.time_in)

    def test_template(self):
        name = 'TemplateTest'

        template_id = self.client.add_template(name, 'Hello')
        self.assertIsNotNone(template_id)

        template_list = self.client.get_templates()
        exists = False
        for template in template_list:
            if template.name == name:
                exists = True
                break

        if not exists:
            raise Exception

        result = self.client.delete_template(name)
        self.assertEqual(result, 'deleted')

        template_list = self.client.get_templates()
        exists = False
        for template in template_list:
            if template.name == name:
                exists = True
                break

        if exists:
            raise Exception

    def test_statistic(self):
        for stat in self.client.get_statistic_on_month(2016, 7):
            self.assertIsInstance(stat, models.Statistic)

    def test_hlr_request(self):
        for hlr in self.client.make_hlr_request('79140000000'):
            self.assertIsInstance(hlr, models.HLRResponse)

    def test_hlr_statistic(self):
        from_date, to_date = '2016-01-01', '2016-09-01'
        for statistic in self.client.get_hlr_statistic(from_date, to_date):
            self.assertIsInstance(statistic, models.HLRStatistic)

    def test_network_by_phone(self):
        result = self.client.get_network_by_phone('79140000000')
        self.assertIsInstance(result, models.Operator)

    def test_inbox_messages(self):
        date_from = '2016-01-01'
        try:
            self.client.get_inbox_messages(date_from)
        except IntisApiError:
            pass

    def test_price(self):
        for price in self.client.get_prices():
            self.assertIsInstance(price, models.Price)


if __name__ == '__main__':
    unittest.main()
