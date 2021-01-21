import json

from django.test import TestCase, override_settings

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

    def test_get_current_metal_value_aggregator(self):
        total_silver_value = (int(self.silver_test_obj_1.amount) + int(self.silver_test_obj_2.amount)) * metal_prices.get('silver')
        total_gold_value = (int(self.gold_test_obj_1.amount) + int(self.gold_test_obj_2.amount)) * metal_prices.get('gold')
        total_metal_value = total_silver_value + total_gold_value

        self.assertEqual(self.a.get_current_metal_value(name='silver'), total_silver_value)
        self.assertEqual(self.a.get_current_metal_value(name='gold'), total_gold_value)
        self.assertEqual(self.a.get_current_metal_value(), total_metal_value)

    def test_get_metal_cash_spend(self):
        cash_silver_spend = self.silver_test_obj_1.bought_price.amount + self.silver_test_obj_2.bought_price.amount
        cash_gold_spend = self.gold_test_obj_1.bought_price.amount + self.gold_test_obj_2.bought_price.amount
        cash_metal_spend = cash_silver_spend + cash_gold_spend

        self.assertEqual(self.a.get_metal_cash_spend(name='silver'), cash_silver_spend)
        self.assertEqual(self.a.get_metal_cash_spend(name='gold'), cash_gold_spend)
        self.assertEqual(self.a.get_metal_cash_spend(), cash_metal_spend)

    def test_get_my_cash_aggregator(self):
        my_cash = self.cash_test_obj_1.my_cash.amount + self.cash_test_obj_2.my_cash.amount
        self.assertEqual(self.a.get_my_cash(), my_cash)

    def test_get_currency_value(self):
        total_usd = currency_prices.get('USD') * (self.usd_test_obj_1.bought_currency.amount + self.usd_test_obj_2.bought_currency.amount)
        total_eur = currency_prices.get('EUR') * (self.eur_test_obj_1.bought_currency.amount + self.eur_test_obj_2.bought_currency.amount)
        total_chf = currency_prices.get('CHF') * (self.chf_test_obj_1.bought_currency.amount + self.chf_test_obj_2.bought_currency.amount)

        self.assertEqual(self.a.get_currency_value(name='USD'), total_usd.__round__(2))
        self.assertEqual(self.a.get_currency_value(name='EUR'), total_eur.__round__(2))
        self.assertEqual(self.a.get_currency_value(name='CHF'), total_chf.__round__(2))

