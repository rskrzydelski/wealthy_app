import json

from django.test import TestCase, override_settings

from resources.models import Currency
from accounts.models import InvestorUser


class CurrencyModelTestCase(TestCase):
    @override_settings(USE_TZ=False)
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

    def test_currency_usd_check_fields(self):
        self.assertEqual(str(self.usd_test_obj_1.bought_price.amount), self.usd_test_data_1.get('bought_price'))
        self.assertEqual(self.usd_test_obj_1.bought_price_currency, self.usd_test_data_1.get('bought_price_currency'))
        self.assertEqual(self.usd_test_obj_1.date_of_bought, self.usd_test_data_1.get('date_of_bought'))
        self.assertEqual(str(self.usd_test_obj_1.bought_currency.amount), self.usd_test_data_1.get('bought_currency'))
        self.assertEqual(self.usd_test_obj_1.bought_currency_currency, self.usd_test_data_1.get('bought_currency_currency'))

    def test_currency_eur_check_fields(self):
        self.assertEqual(str(self.eur_test_obj_1.bought_price.amount), self.eur_test_data_1.get('bought_price'))
        self.assertEqual(self.eur_test_obj_1.bought_price_currency, self.eur_test_data_1.get('bought_price_currency'))
        self.assertEqual(self.eur_test_obj_1.date_of_bought, self.eur_test_data_1.get('date_of_bought'))
        self.assertEqual(str(self.eur_test_obj_1.bought_currency.amount), self.eur_test_data_1.get('bought_currency'))
        self.assertEqual(self.eur_test_obj_1.bought_currency_currency, self.eur_test_data_1.get('bought_currency_currency'))

    def test_currency_chf_check_fields(self):
        self.assertEqual(str(self.chf_test_obj_1.bought_price.amount), self.chf_test_data_1.get('bought_price'))
        self.assertEqual(self.chf_test_obj_1.bought_price_currency, self.chf_test_data_1.get('bought_price_currency'))
        self.assertEqual(self.chf_test_obj_1.date_of_bought, self.chf_test_data_1.get('date_of_bought'))
        self.assertEqual(str(self.chf_test_obj_1.bought_currency.amount), self.chf_test_data_1.get('bought_currency'))
        self.assertEqual(self.chf_test_obj_1.bought_currency_currency, self.chf_test_data_1.get('bought_currency_currency'))

    def test_currency_manager_list_len(self):
        qs = Currency.objects.get_currency_list(owner=self.investor_test)
        self.assertEqual(qs.count(), 6)

    def test_currency_manager_list_content(self):
        qs = Currency.objects.get_currency_list(owner=self.investor_test)

        self.assertTrue(qs.filter(bought_currency_currency='USD').filter(bought_currency=560).exists() is True)
        self.assertTrue(qs.filter(bought_currency_currency='USD').filter(bought_currency=2700).exists() is True)
        self.assertTrue(qs.filter(bought_currency_currency='EUR').filter(bought_currency=1000).exists() is True)
        self.assertTrue(qs.filter(bought_currency_currency='EUR').filter(bought_currency=250).exists() is True)
        self.assertTrue(qs.filter(bought_currency_currency='CHF').filter(bought_currency=200).exists() is True)
        self.assertTrue(qs.filter(bought_currency_currency='CHF').filter(bought_currency=700).exists() is True)

    def test_currency_manager_usd_list_len(self):
        qs = Currency.objects.get_currency_list(owner=self.investor_test, currency='USD')
        self.assertEqual(qs.count(), 2)

    def test_currency_manager_usd_content(self):
        qs = Currency.objects.get_currency_list(owner=self.investor_test, currency='USD')

        self.assertTrue(qs.filter(bought_currency_currency='USD').filter(bought_currency=560).exists() is True)
        self.assertTrue(qs.filter(bought_currency_currency='USD').filter(bought_currency=2700).exists() is True)

    def test_currency_manager_eur_list_len(self):
        qs = Currency.objects.get_currency_list(owner=self.investor_test, currency='EUR')
        self.assertEqual(qs.count(), 2)

    def test_currency_manager_eur_content(self):
        qs = Currency.objects.get_currency_list(owner=self.investor_test, currency='EUR')

        self.assertTrue(qs.filter(bought_currency_currency='EUR').filter(bought_currency=1000).exists() is True)
        self.assertTrue(qs.filter(bought_currency_currency='EUR').filter(bought_currency=250).exists() is True)

    def test_currency_manager_chf_list_len(self):
        qs = Currency.objects.get_currency_list(owner=self.investor_test, currency='CHF')
        self.assertEqual(qs.count(), 2)

    def test_currency_manager_chf_content(self):
        qs = Currency.objects.get_currency_list(owner=self.investor_test, currency='CHF')

        self.assertTrue(qs.filter(bought_currency_currency='CHF').filter(bought_currency=200).exists() is True)
        self.assertTrue(qs.filter(bought_currency_currency='CHF').filter(bought_currency=700).exists() is True)

    def test_currency_manager_list_negative_name(self):
        qs = Currency.objects.get_currency_list(owner=self.investor_test, currency='abcd')
        self.assertTrue(not qs)

    def test_currency_manager_total(self):
        total_currency = Currency.objects.get_total_currency(owner=self.investor_test, currency=None)
        self.assertEqual(total_currency, None)

    def test_currency_manager_total_usd(self):
        currency = Currency.objects.get_total_currency(owner=self.investor_test, currency='USD')
        self.assertEqual(currency, 3260)

    def test_currency_manager_total_eur(self):
        currency = Currency.objects.get_total_currency(owner=self.investor_test, currency='EUR')
        self.assertEqual(currency, 1250)

    def test_currency_manager_total_chf(self):
        currency = Currency.objects.get_total_currency(owner=self.investor_test, currency='CHF')
        self.assertEqual(currency, 900)

    def test_currency_manager_total_negative_name(self):
        currency = Currency.objects.get_total_currency(owner=self.investor_test, currency='abcd')
        self.assertEqual(currency, 0)

