import json
from decimal import Decimal

from django.test import TestCase

from rest_framework.test import RequestsClient

from accounts.models import InvestorUser
from resources.models import Metal


class MetalApiTestCase(TestCase):
    def setUp(self):
        with open("./resources/tests/cfg/test_metal_data.config", "r") as metal_cfg:
            test_data = metal_cfg.read()

        self.investor_test = InvestorUser.objects.create_user(username='testuser', password='abc123')
        self.metal_test_data = json.loads(test_data)

        self.silver_test_data_1 = self.metal_test_data.get('silver_record_1')
        self.silver_test_data_2 = self.metal_test_data.get('silver_record_2')
        self.gold_test_data_1 = self.metal_test_data.get('gold_record_1')
        self.gold_test_data_2 = self.metal_test_data.get('gold_record_2')

        self.silver_test_obj_1 = Metal.objects.create(owner=self.investor_test, **self.silver_test_data_1)
        self.silver_test_obj_2 = Metal.objects.create(owner=self.investor_test, **self.silver_test_data_2)
        self.gold_test_obj_1 = Metal.objects.create(owner=self.investor_test, **self.gold_test_data_1)
        self.gold_test_obj_2 = Metal.objects.create(owner=self.investor_test, **self.gold_test_data_2)

        self.client = RequestsClient()
        response = self.client.post('http://127.0.0.1:8000/api/v1/auth/token', json={'username': 'testuser',
                                                                                     'password': 'abc123'})
        content = json.loads(response.content.decode('utf-8'))
        self.token = content.get('token')

    def test_len_get_metal_list(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/metals',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(self.metal_test_data), len(response_content))

    def test_content_get_metal_list(self):
        reference_data = []
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/metals',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))

        for item in self.metal_test_data.values():
            del item['description']
            reference_data.append(item)

        response_content.sort(key=lambda d: int(d['amount']))
        reference_data.sort(key=lambda d: int(d['amount']))

        response_js = json.dumps(response_content, sort_keys=True)
        reference_js = json.dumps(reference_data, sort_keys=True)

        self.assertEqual(response_js, reference_js)

    def test_len_get_metal_list_silver(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/metals?name=silver',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(2, len(response_content))

    def test_content_get_metal_list_silver(self):
        reference_data = []
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/metals?name=silver',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))

        for item in self.metal_test_data.values():
            del item['description']
            if item['name'] == 'gold':
                continue
            reference_data.append(item)

        response_content.sort(key=lambda d: int(d['amount']))
        reference_data.sort(key=lambda d: int(d['amount']))

        response_js = json.dumps(response_content, sort_keys=True)
        reference_js = json.dumps(reference_data, sort_keys=True)

        self.assertEqual(response_js, reference_js)

    def test_len_get_metal_list_gold(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/metals?name=gold',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(2, len(response_content))

    def test_content_get_metal_list_gold(self):
        reference_data = []
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/metals?name=gold',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))

        for item in self.metal_test_data.values():
            del item['description']
            if item['name'] == 'silver':
                continue
            reference_data.append(item)

        response_content.sort(key=lambda d: int(d['amount']))
        reference_data.sort(key=lambda d: int(d['amount']))

        response_js = json.dumps(response_content, sort_keys=True)
        reference_js = json.dumps(reference_data, sort_keys=True)

        self.assertEqual(response_js, reference_js)

    def test_sum_content_get_silver(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/metals?name=silver&sum=true',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        amount_sum = str(int(self.silver_test_data_1.get('amount')) + int(self.silver_test_data_2.get('amount')))
        total_cash_spend = Decimal(self.silver_test_data_1.get('bought_price')) + \
                           Decimal(self.silver_test_data_2.get('bought_price'))

        self.assertEqual(response_content[0]['total_amount'], amount_sum)
        self.assertEqual(response_content[0]['total_cash_spend'], str(total_cash_spend.to_integral()))

    def test_sum_content_get_gold(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/metals?name=gold&sum=true',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        amount_sum = str(int(self.gold_test_data_1.get('amount')) + int(self.gold_test_data_2.get('amount')))
        total_cash_spend = Decimal(self.gold_test_data_1.get('bought_price')) + \
                           Decimal(self.gold_test_data_2.get('bought_price'))

        self.assertEqual(response_content[0]['total_amount'], amount_sum)
        self.assertEqual(response_content[0]['total_cash_spend'], str(total_cash_spend.to_integral()))

    def test_incorrect_query_get_metal_list(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/metals?name=abcd',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertTrue(not response_content)

    def test_metal_detail(self):
        silver = Metal.objects.filter(name='silver')
        response = self.client.get('http://127.0.0.1:8000/api/v1/resources/metals/{}'.format(silver[0].id),
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        name = response_content.get('name')

        self.assertEqual(200, response.status_code)
        self.assertEqual('silver', name)

    def test_create_gold(self):
        response = self.client.post('http://127.0.0.1:8000/api/v1/resources/metals',
                                    json={'name': 'gold',
                                          'bought_price': '20000',
                                          'amount': '4',
                                          'unit': 'oz',
                                          'date_of_bought': '2019-11-26T11:00:30Z',
                                          'description': 'test gold create'},
                                    headers={'Authorization': 'JWT %s' % self.token})
        g = Metal.objects.filter(description='test gold create').first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(g.name, 'gold')
        self.assertEqual(g.bought_price.amount, 20000.00)
        self.assertEqual(g.amount, 4)
        self.assertEqual(g.unit, 'oz')
        self.assertEqual(g.date_of_bought.strftime('%Y-%m-%d, %H:%M:%S'), '2019-11-26, 11:00:30')
        self.assertEqual(g.description, 'test gold create')

    def test_create_silver(self):
        response = self.client.post('http://127.0.0.1:8000/api/v1/resources/metals',
                                    json={'name': 'silver',
                                          'bought_price': '12300',
                                          'amount': '134',
                                          'unit': 'oz',
                                          'date_of_bought': '2019-11-26T11:00:30Z',
                                          'description': 'test silver create'},
                                    headers={'Authorization': 'JWT %s' % self.token})
        g = Metal.objects.filter(description='test silver create').first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(g.name, 'silver')
        self.assertEqual(g.bought_price.amount, 12300.00)
        self.assertEqual(g.amount, 134)
        self.assertEqual(g.unit, 'oz')
        self.assertEqual(g.date_of_bought.strftime('%Y-%m-%d, %H:%M:%S'), '2019-11-26, 11:00:30')
        self.assertEqual(g.description, 'test silver create')

    def test_silver_delete(self):
        pk = self.silver_test_obj_1.pk
        response = self.client.delete('http://127.0.0.1:8000/api/v1/resources/metals/%s' % pk,
                                      headers={'Authorization': 'JWT %s' % self.token})

        try:
            Metal.objects.get(description=self.silver_test_obj_1.description)
        except Metal.DoesNotExist:
            object_status = 404

        self.assertEquals(response.status_code, 204)
        self.assertEquals(object_status, 404)

    def test_gold_delete(self):
        pk = self.gold_test_obj_1.pk
        response = self.client.delete('http://127.0.0.1:8000/api/v1/resources/metals/%s' % pk,
                                      headers={'Authorization': 'JWT %s' % self.token})

        try:
            Metal.objects.get(description=self.gold_test_obj_1.description)
        except Metal.DoesNotExist:
            object_status = 404

        self.assertEquals(response.status_code, 204)
        self.assertEquals(object_status, 404)
