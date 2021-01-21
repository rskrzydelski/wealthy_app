import json

from django.test import TestCase, override_settings

from resources.models import Cash
from accounts.models import InvestorUser


class CashModelTestCase(TestCase):
    @override_settings(USE_TZ=False)
    def setUp(self):
        with open("./resources/tests/cfg/test_cash_data.config", "r") as cash_cfg:
            test_data = cash_cfg.read()

        self.investor_test = InvestorUser.objects.create_user(username='testuser', password='abc123')
        # self.my_currency = self.investor_test.my_currency
        self.cash_test_data = json.loads(test_data)

        self.cash_test_data_1 = self.cash_test_data.get('cash_record_1')
        self.cash_test_data_2 = self.cash_test_data.get('cash_record_2')

        self.cash_test_obj_1 = Cash.objects.create(owner=self.investor_test, **self.cash_test_data_1)
        self.cash_test_obj_2 = Cash.objects.create(owner=self.investor_test, **self.cash_test_data_2)

    def test_cash_check_fields(self):
        self.assertEqual(self.cash_test_obj_1.save_date, self.cash_test_data_1.get('save_date'))
        self.assertEqual(str(self.cash_test_obj_1.my_cash.amount), self.cash_test_data_1.get('my_cash'))
        self.assertEqual(self.cash_test_obj_1.my_cash_currency, self.cash_test_data_1.get('my_cash_currency'))

    def test_cash_manager_list_len(self):
        qs = Cash.objects.get_cash_list(owner=self.investor_test)
        self.assertEqual(qs.count(), 2)

    def test_cash_manager_list_content(self):
        qs = Cash.objects.get_cash_list(owner=self.investor_test)

        self.assertTrue(qs.filter(my_cash=10000).exists() is True)
        self.assertTrue(qs.filter(my_cash=3000).exists() is True)

    def test_cash_manager_total_cash(self):
        cash = Cash.objects.get_total_cash(owner=self.investor_test)
        self.assertEqual(cash, 13000)
