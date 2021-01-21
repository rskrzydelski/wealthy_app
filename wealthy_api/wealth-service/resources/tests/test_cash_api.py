import json
from decimal import Decimal

from django.test import TestCase, override_settings

from rest_framework.test import RequestsClient

from accounts.models import InvestorUser
from resources.models import Cash


class CashApiTestCase(TestCase):
    def setUp(self):
        with open("./resources/tests/cfg/test_cash_data.config", "r") as cash_cfg:
            test_data = cash_cfg.read()

        self.investor_test = InvestorUser.objects.create_user(username='testuser', password='abc123')
        self.cash_test_data = json.loads(test_data)

        self.cash_test_data_1 = self.cash_test_data.get('cash_record_1')
        self.cash_test_data_2 = self.cash_test_data.get('cash_record_2')

        self.cash_test_obj_1 = Cash.objects.create(owner=self.investor_test, **self.cash_test_data_1)
        self.cash_test_obj_2 = Cash.objects.create(owner=self.investor_test, **self.cash_test_data_2)

        self.client = RequestsClient()
        response = self.client.post('http://127.0.0.1:8000/api/v1/auth/token', json={'username': 'testuser',
                                                                                     'password': 'abc123'})
        content = json.loads(response.content.decode('utf-8'))
        self.token = content.get('token')

    def test_len_get_cash_list(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/cash',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(self.cash_test_data), len(response_content))

    def test_content_get_cash_list(self):
        reference_data = []
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/cash',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))

        for item in self.cash_test_data.values():
            item['my_cash'] = item['my_cash'] + '.00'
            if item['my_cash_currency'] == self.investor_test.my_currency:
                item['my_currency'] = self.investor_test.my_currency
                del item['my_cash_currency']
            item['save_date'] = item['save_date'][:item['save_date'].index(' ')] + 'T' + item['save_date'][item['save_date'].index(' ') + 1:] + 'Z'
            reference_data.append(item)

        response_content.sort(key=lambda d: Decimal(d['my_cash']))
        reference_data.sort(key=lambda d: Decimal(d['my_cash']))

        response_js = json.dumps(response_content, sort_keys=True)
        reference_js = json.dumps(reference_data, sort_keys=True)
        self.assertEqual(response_js, reference_js)

    def test_sum_content_get_cash(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/cash?sum=true',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))

        cash_sum = str(int(self.cash_test_data_1.get('my_cash')) + int(self.cash_test_data_2.get('my_cash')))
        self.assertEqual(response_content[0]['total_cash'], cash_sum)

    def test_incorrect_query_get_cash_list(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/cash?sum=abcd',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertTrue(not response_content)

    def test_create_cash(self):
        response = self.client.post('http://127.0.0.1:8000/api/v1/resources/cash',
                                    json={'my_cash': '1234',
                                          'my_currency': 'PLN',
                                          'save_date': '2019-11-26T11:00:30Z'},
                                    headers={'Authorization': 'JWT %s' % self.token})
        g = Cash.objects.filter(my_cash='1234').first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(g.my_cash_currency, 'PLN')
        self.assertEqual(g.my_cash.amount, 1234.00)
        self.assertEqual(g.save_date.strftime('%Y-%m-%d, %H:%M:%S'), '2019-11-26, 11:00:30')

    def test_cash_delete(self):
        pk = self.cash_test_obj_1.pk
        response = self.client.delete('http://127.0.0.1:8000/api/v1/resources/cash/%s' % pk,
                                      headers={'Authorization': 'JWT %s' % self.token})

        try:
            Cash.objects.get(save_date=self.cash_test_obj_1.save_date)
        except Cash.DoesNotExist:
            object_status = 404

        self.assertEquals(response.status_code, 204)
        self.assertEquals(object_status, 404)
