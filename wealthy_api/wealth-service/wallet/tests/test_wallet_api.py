import json
from decimal import Decimal

from django.test import TestCase, override_settings

from rest_framework.test import RequestsClient

from resources.models import Metal, Currency, Cash
from wallet.aggregators import Aggregator, metal_prices, currency_prices
from accounts.models import InvestorUser


class AggregatorTestCase(TestCase):
    @override_settings(USE_TZ=False)
    def setUp(self):
        with open("./wallet/tests/cfg/test_data.config", "r") as data_cfg:
            test_data = data_cfg.read()

        self.investor_test = InvestorUser.objects.create_user(username='testuser', password='abc123')
        self.js_test_data = json.loads(test_data)

        self.a = Aggregator(owner=self.investor_test)

        # collect data
        self.silver_test_data_1 = self.js_test_data.get('silver_record_1')
        self.silver_test_data_2 = self.js_test_data.get('silver_record_2')
        self.gold_test_data_1 = self.js_test_data.get('gold_record_1')
        self.gold_test_data_2 = self.js_test_data.get('gold_record_2')
        self.cash_test_data_1 = self.js_test_data.get('cash_record_1')
        self.cash_test_data_2 = self.js_test_data.get('cash_record_2')
        self.usd_test_data_1 = self.js_test_data.get('usd_record_1')
        self.usd_test_data_2 = self.js_test_data.get('usd_record_2')
        self.eur_test_data_1 = self.js_test_data.get('eur_record_1')
        self.eur_test_data_2 = self.js_test_data.get('eur_record_2')
        self.chf_test_data_1 = self.js_test_data.get('chf_record_1')
        self.chf_test_data_2 = self.js_test_data.get('chf_record_2')

        # collect resources
        self.silver_test_obj_1 = Metal.objects.create(owner=self.investor_test, **self.silver_test_data_1)
        self.silver_test_obj_2 = Metal.objects.create(owner=self.investor_test, **self.silver_test_data_2)
        self.gold_test_obj_1 = Metal.objects.create(owner=self.investor_test, **self.gold_test_data_1)
        self.gold_test_obj_2 = Metal.objects.create(owner=self.investor_test, **self.gold_test_data_2)
        self.usd_test_obj_1 = Currency.objects.create(owner=self.investor_test, **self.usd_test_data_1)
        self.usd_test_obj_2 = Currency.objects.create(owner=self.investor_test, **self.usd_test_data_2)
        self.eur_test_obj_1 = Currency.objects.create(owner=self.investor_test, **self.eur_test_data_1)
        self.eur_test_obj_2 = Currency.objects.create(owner=self.investor_test, **self.eur_test_data_2)
        self.chf_test_obj_1 = Currency.objects.create(owner=self.investor_test, **self.chf_test_data_1)
        self.chf_test_obj_2 = Currency.objects.create(owner=self.investor_test, **self.chf_test_data_2)
        self.cash_test_obj_1 = Cash.objects.create(owner=self.investor_test, **self.cash_test_data_1)
        self.cash_test_obj_2 = Cash.objects.create(owner=self.investor_test, **self.cash_test_data_2)

        self.client = RequestsClient()
        response = self.client.post('http://127.0.0.1:8000/api/v1/auth/token', json={'username': 'testuser',
                                                                                     'password': 'abc123'})
        content = json.loads(response.content.decode('utf-8'))
        self.token = content.get('token')

    def test_my_fortune(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/wallet',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))

        total_silver = metal_prices.get('silver') * Metal.objects.get_total_metal_amount(owner=self.investor_test, name='silver')
        total_gold = metal_prices.get('gold') * Metal.objects.get_total_metal_amount(owner=self.investor_test, name='gold')
        total_cash = Cash.objects.get_total_cash(owner=self.investor_test)
        total_usd = currency_prices.get('USD') * Currency.objects.get_total_currency(owner=self.investor_test, currency='usd')
        total_eur = currency_prices.get('EUR') * Currency.objects.get_total_currency(owner=self.investor_test, currency='eur')
        total_chf = currency_prices.get('CHF') * Currency.objects.get_total_currency(owner=self.investor_test, currency='chf')

        my_fortune = total_silver + total_gold + \
                     total_cash + \
                     total_usd.to_integral() + total_eur.to_integral() + total_chf.to_integral()
        self.assertEquals(response_content.get('my_fortune'), str(my_fortune) + '.00')

    def test_my_metals_value(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/wallet/metal',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))

        calc_value = Decimal(self.silver_test_obj_1.amount) * Decimal(metal_prices.get('silver')) + \
                     Decimal(self.silver_test_obj_2.amount) * Decimal(metal_prices.get('silver')) + \
                     Decimal(self.gold_test_obj_1.amount) * Decimal(metal_prices.get('gold')) + \
                     Decimal(self.gold_test_obj_2.amount) * Decimal(metal_prices.get('gold'))

        calc_spend_cash = Decimal(self.silver_test_obj_1.bought_price.amount) + \
                          Decimal(self.silver_test_obj_2.bought_price.amount) + \
                          Decimal(self.gold_test_obj_1.bought_price.amount) + \
                          Decimal(self.gold_test_obj_2.bought_price.amount)

        self.assertEquals(Decimal(response_content.get('total_cash')), calc_value)
        self.assertEquals(response_content.get('name'), 'All metals')
        self.assertEquals(Decimal(response_content.get('total_cash_spend')), calc_spend_cash)
        self.assertEquals(Decimal(response_content.get('profit')), calc_value - calc_spend_cash)

    def test_my_silver_value(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/wallet/metal/silver',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        calc_value = Decimal(self.silver_test_obj_1.amount) * Decimal(metal_prices.get('silver')) + \
                     Decimal(self.silver_test_obj_2.amount) * Decimal(metal_prices.get('silver'))

        calc_spend_cash = Decimal(self.silver_test_obj_1.bought_price.amount) + \
                          Decimal(self.silver_test_obj_2.bought_price.amount)

        self.assertEquals(Decimal(response_content.get('total_cash')), calc_value)
        self.assertEquals(response_content.get('name'), 'silver')
        self.assertEquals(Decimal(response_content.get('total_cash_spend')), calc_spend_cash)
        self.assertEquals(Decimal(response_content.get('profit')), calc_value - calc_spend_cash)

    def test_my_gold_value(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/wallet/metal/gold',
                                   headers={'Authorization': 'JWT %s' % self.token})
        response_content = json.loads(response.content.decode('utf-8'))
        calc_value = Decimal(self.gold_test_obj_1.amount) * Decimal(metal_prices.get('gold')) + \
                     Decimal(self.gold_test_obj_2.amount) * Decimal(metal_prices.get('gold'))

        calc_spend_cash = Decimal(self.gold_test_obj_1.bought_price.amount) + \
                          Decimal(self.gold_test_obj_2.bought_price.amount)

        self.assertEquals(Decimal(response_content.get('total_cash')), calc_value)
        self.assertEquals(response_content.get('name'), 'gold')
        self.assertEquals(Decimal(response_content.get('total_cash_spend')), calc_spend_cash)
        self.assertEquals(Decimal(response_content.get('profit')), calc_value - calc_spend_cash)
