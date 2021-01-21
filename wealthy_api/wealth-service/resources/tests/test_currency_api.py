import json
from decimal import Decimal

from django.test import TestCase, override_settings

from rest_framework.test import RequestsClient

from accounts.models import InvestorUser
from resources.models import Currency


class CurrencyApiTestCase(TestCase):
    def setUp(self):
        with open("./resources/tests/cfg/test_currency_data.config", "r") as currency_cfg:
            test_data = currency_cfg.read()

        self.investor_test = InvestorUser.objects.create_user(username='testuser', password='abc123')
        self.currency_test_data = json.loads(test_data)

        self.usd_test_data_1 = self.currency_test_data.get('usd_record_1')
        self.usd_test_data_2 = self.currency_test_data.get('usd_record_2')

        self.eur_test_data_1 = self.currency_test_data.get('eur_record_1')
        self.eur_test_data_2 = self.currency_test_data.get('eur_record_2')

        self.chf_test_data_1 = self.currency_test_data.get('chf_record_1')
        self.chf_test_data_2 = self.currency_test_data.get('chf_record_2')

        self.usd_test_obj_1 = Currency.objects.create(owner=self.investor_test, **self.usd_test_data_1)
        self.usd_test_obj_2 = Currency.objects.create(owner=self.investor_test, **self.usd_test_data_2)

        self.eur_test_obj_1 = Currency.objects.create(owner=self.investor_test, **self.eur_test_data_1)
        self.eur_test_obj_2 = Currency.objects.create(owner=self.investor_test, **self.eur_test_data_2)

        self.chf_test_obj_1 = Currency.objects.create(owner=self.investor_test, **self.chf_test_data_1)
        self.chf_test_obj_2 = Currency.objects.create(owner=self.investor_test, **self.chf_test_data_2)

        self.client = RequestsClient()
        response = self.client.post('http://127.0.0.1:8000/api/v1/auth/token', json={'username': 'testuser',
                                                                                     'password': 'abc123'})
        content = json.loads(response.content.decode('utf-8'))
        self.token = content.get('token')

    def test_len_get_currency_list(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/currency',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(len(self.currency_test_data), len(response_content))

    def test_content_get_currency_list(self):
        reference_data = []
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/currency',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))

        for item in self.currency_test_data.values():
            item['currency'] = item['bought_currency_currency']
            del item['bought_currency_currency']
            del item['bought_price_currency']
            item['bought_currency'] = item['bought_currency'] + '.00'
            item['bought_price'] = item['bought_price'] + '.00'
            item['date_of_bought'] = item['date_of_bought'][:item['date_of_bought'].index(' ')] + 'T' + item['date_of_bought'][item['date_of_bought'].index(' ') + 1:] + 'Z'
            reference_data.append(item)
        response_content.sort(key=lambda d: Decimal(d['bought_currency']))
        reference_data.sort(key=lambda d: Decimal(d['bought_currency']))

        response_js = json.dumps(response_content, sort_keys=True)
        reference_js = json.dumps(reference_data, sort_keys=True)

        self.assertEqual(response_js, reference_js)

    def test_len_get_currency_list_usd(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/currency?name=usd',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(2, len(response_content))

    def test_content_get_currency_list_usd(self):
        qs = Currency.objects.filter(bought_currency_currency='USD')
        self.assertEqual(qs[0].bought_currency_currency, 'USD')
        self.assertEqual(qs[1].bought_currency_currency, 'USD')

    def test_len_get_currency_list_eur(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/currency?name=eur',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(2, len(response_content))

    def test_content_get_currency_list_eur(self):
        qs = Currency.objects.filter(bought_currency_currency='EUR')
        self.assertEqual(qs[0].bought_currency_currency, 'EUR')
        self.assertEqual(qs[1].bought_currency_currency, 'EUR')

    def test_len_get_currency_list_chf(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/currency?name=chf',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(2, len(response_content))

    def test_content_get_currency_list_chf(self):
        qs = Currency.objects.filter(bought_currency_currency='CHF')
        self.assertEqual(qs[0].bought_currency_currency, 'CHF')
        self.assertEqual(qs[1].bought_currency_currency, 'CHF')

    def test_len_get_currency_list_pln(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/currency?name=pln',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(0, len(response_content))

    def test_sum_content_get_usd(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/currency?name=usd&sum=true',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        currency_sum = str(int(self.usd_test_data_1.get('bought_currency')) + int(self.usd_test_data_2.get('bought_currency')))
        self.assertEqual(response_content[0]['total_currency'], currency_sum)

    def test_sum_content_get_eur(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/currency?name=eur&sum=true',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        currency_sum = str(int(self.eur_test_data_1.get('bought_currency')) + int(self.eur_test_data_2.get('bought_currency')))
        self.assertEqual(response_content[0]['total_currency'], currency_sum)

    def test_sum_content_get_chf(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/currency?name=chf&sum=true',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        currency_sum = str(int(self.chf_test_data_1.get('bought_currency')) + int(self.chf_test_data_2.get('bought_currency')))
        self.assertEqual(response_content[0]['total_currency'], currency_sum)

    def test_incorrect_query_get_currency_list(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/currency?name=abcd',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertTrue(not response_content)

    def test_currency_detail(self):
        usd = Currency.objects.filter(bought_currency_currency='USD')
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/currency/{}'.format(usd[0].id),
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        currency = response_content.get('currency')

        self.assertEqual(200, response.status_code)
        self.assertEqual('USD', currency)

    def test_create_usd(self):
        response = self.client.post('http://127.0.0.1:8000/api/v1/resources/currency',
                                    json={'bought_currency': '5000',
                                          'bought_currency_currency': 'USD',
                                          'bought_price': '20000',
                                          'bought_price_currency': 'PLN',
                                          'date_of_bought': '2019-11-26T11:00:30Z'},
                                    headers={'Authorization': 'JWT %s' % self.token})
        g = Currency.objects.filter(bought_price='20000').first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(g.bought_currency_currency, 'USD')
        self.assertEqual(g.bought_currency.amount, 5000.00)
        self.assertEqual(g.bought_price.amount, 20000.00)
        self.assertEqual(g.bought_price_currency, 'PLN')
        self.assertEqual(g.date_of_bought.strftime('%Y-%m-%d, %H:%M:%S'), '2019-11-26, 11:00:30')

    def test_create_eur(self):
        response = self.client.post('http://127.0.0.1:8000/api/v1/resources/currency',
                                    json={'bought_currency': '5000',
                                          'bought_currency_currency': 'EUR',
                                          'bought_price': '20001',
                                          'bought_price_currency': 'PLN',
                                          'date_of_bought': '2019-11-26T11:00:30Z'},
                                    headers={'Authorization': 'JWT %s' % self.token})
        g = Currency.objects.filter(bought_price='20001').first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(g.bought_currency_currency, 'EUR')
        self.assertEqual(g.bought_currency.amount, 5000.00)
        self.assertEqual(g.bought_price.amount, 20001.00)
        self.assertEqual(g.bought_price_currency, 'PLN')
        self.assertEqual(g.date_of_bought.strftime('%Y-%m-%d, %H:%M:%S'), '2019-11-26, 11:00:30')

    def test_create_chf(self):
        response = self.client.post('http://127.0.0.1:8000/api/v1/resources/currency',
                                    json={'bought_currency': '5000',
                                          'bought_currency_currency': 'CHF',
                                          'bought_price': '20002',
                                          'bought_price_currency': 'PLN',
                                          'date_of_bought': '2019-11-26T11:00:30Z'},
                                    headers={'Authorization': 'JWT %s' % self.token})
        g = Currency.objects.filter(bought_price='20002').first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(g.bought_currency_currency, 'CHF')
        self.assertEqual(g.bought_currency.amount, 5000.00)
        self.assertEqual(g.bought_price.amount, 20002.00)
        self.assertEqual(g.bought_price_currency, 'PLN')
        self.assertEqual(g.date_of_bought.strftime('%Y-%m-%d, %H:%M:%S'), '2019-11-26, 11:00:30')

    def test_create_pln(self):
        response = self.client.post('http://127.0.0.1:8000/api/v1/resources/currency',
                                    json={'bought_currency': '5000',
                                          'bought_currency_currency': 'PLN',
                                          'bought_price': '20003',
                                          'bought_price_currency': 'PLN',
                                          'date_of_bought': '2019-11-26T11:00:30Z'},
                                    headers={'Authorization': 'JWT %s' % self.token})
        self.assertEqual(response.status_code, 400)

    def test_usd_delete(self):
        pk = self.usd_test_obj_1.pk
        response = self.client.delete('http://127.0.0.1:8000/api/v1/resources/currency/%s' % pk,
                                      headers={'Authorization': 'JWT %s' % self.token})

        try:
            Currency.objects.get(date_of_bought=self.usd_test_obj_1.date_of_bought)
        except Currency.DoesNotExist:
            object_status = 404

        self.assertEquals(response.status_code, 204)
        self.assertEquals(object_status, 404)

    def test_eur_delete(self):
        pk = self.eur_test_obj_1.pk
        response = self.client.delete('http://127.0.0.1:8000/api/v1/resources/currency/%s' % pk,
                                      headers={'Authorization': 'JWT %s' % self.token})

        try:
            Currency.objects.get(date_of_bought=self.eur_test_obj_1.date_of_bought)
        except Currency.DoesNotExist:
            object_status = 404

        self.assertEquals(response.status_code, 204)
        self.assertEquals(object_status, 404)

    def test_chf_delete(self):
        pk = self.chf_test_obj_1.pk
        response = self.client.delete('http://127.0.0.1:8000/api/v1/resources/currency/%s' % pk,
                                      headers={'Authorization': 'JWT %s' % self.token})

        try:
            Currency.objects.get(date_of_bought=self.chf_test_obj_1.date_of_bought)
        except Currency.DoesNotExist:
            object_status = 404

        self.assertEquals(response.status_code, 204)
        self.assertEquals(object_status, 404)

