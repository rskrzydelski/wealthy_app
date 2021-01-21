import json

from django.test import TestCase, override_settings

from resources.models import Metal
from accounts.models import InvestorUser


class MetalModelTestCase(TestCase):
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

    def test_metal_silver_check_fields(self):
        self.assertEqual(self.silver_test_obj_1.name, self.silver_test_data_1.get('name'))
        self.assertEqual(str(self.silver_test_obj_1.bought_price.amount), self.silver_test_data_1.get('bought_price'))
        self.assertEqual(self.silver_test_obj_1.date_of_bought, self.silver_test_data_1.get('date_of_bought'))
        self.assertEqual(self.silver_test_obj_1.unit, self.silver_test_data_1.get('unit'))
        self.assertEqual(self.silver_test_obj_1.amount, self.silver_test_data_1.get('amount'))
        self.assertEqual(self.silver_test_obj_1.description, self.silver_test_data_1.get('description'))

    def test_metal_gold_check_fields(self):
        self.assertEqual(self.gold_test_obj_1.name, self.gold_test_data_1.get('name'))
        self.assertEqual(str(self.gold_test_obj_1.bought_price.amount), self.gold_test_data_1.get('bought_price'))
        self.assertEqual(self.gold_test_obj_1.date_of_bought, self.gold_test_data_1.get('date_of_bought'))
        self.assertEqual(self.gold_test_obj_1.unit, self.gold_test_data_1.get('unit'))
        self.assertEqual(self.gold_test_obj_1.amount, self.gold_test_data_1.get('amount'))
        self.assertEqual(self.gold_test_obj_1.description, self.gold_test_data_1.get('description'))

    def test_metal_manager_list_len(self):
        qs = Metal.objects.get_metal_list(owner=self.investor_test)
        self.assertEqual(qs.count(), 4)

    def test_metal_manager_list_content(self):
        qs = Metal.objects.get_metal_list(owner=self.investor_test)

        self.assertTrue(qs.filter(name='silver').filter(amount=130).exists() is True)
        self.assertTrue(qs.filter(name='silver').filter(amount=25).exists() is True)
        self.assertTrue(qs.filter(name='gold').filter(amount=1).exists() is True)
        self.assertTrue(qs.filter(name='gold').filter(amount=3).exists() is True)

    def test_metal_manager_silver_list_len(self):
        qs = Metal.objects.get_metal_list(owner=self.investor_test, name='silver')
        self.assertEqual(qs.count(), 2)

    def test_metal_manager_silver_content(self):
        qs = Metal.objects.get_metal_list(owner=self.investor_test, name='silver')

        self.assertTrue(qs.filter(name='silver').filter(amount=130).exists() is True)
        self.assertTrue(qs.filter(name='silver').filter(amount=25).exists() is True)

    def test_metal_manager_gold_list_len(self):
        qs = Metal.objects.get_metal_list(owner=self.investor_test, name='gold')
        self.assertEqual(qs.count(), 2)

    def test_metal_manager_gold_content(self):
        qs = Metal.objects.get_metal_list(owner=self.investor_test, name='gold')

        self.assertTrue(qs.filter(name='gold').filter(amount=1).exists() is True)
        self.assertTrue(qs.filter(name='gold').filter(amount=3).exists() is True)

    def test_metal_manager_list_negative_name(self):
        qs = Metal.objects.get_metal_list(owner=self.investor_test, name='abcd')
        self.assertTrue(not qs)

    def test_metal_manager_total_amount(self):
        amount = Metal.objects.get_total_metal_amount(owner=self.investor_test)
        self.assertEqual(amount, None)

    def test_metal_manager_total_silver_amount(self):
        amount = Metal.objects.get_total_metal_amount(owner=self.investor_test, name='silver')
        self.assertEqual(amount, 155)

    def test_metal_manager_total_gold_amount(self):
        amount = Metal.objects.get_total_metal_amount(owner=self.investor_test, name='gold')
        self.assertEqual(amount, 4)

    def test_metal_manager_total_amount_negative_name(self):
        amount = Metal.objects.get_total_metal_amount(owner=self.investor_test, name='abcd')
        self.assertEqual(amount, 0)

    def test_metal_manager_silver_cash_spend(self):
        cash = Metal.objects.get_total_metal_cash_spend(owner=self.investor_test, name='silver')
        self.assertEqual(cash, 14400)

    def test_metal_manager_gold_cash_spend(self):
        cash = Metal.objects.get_total_metal_cash_spend(owner=self.investor_test, name='gold')
        self.assertEqual(cash, 24100)

