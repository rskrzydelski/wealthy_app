import sys
from decimal import Decimal

from django.db.models import Sum
from resources.models import Metal, Cash, Crypto
from market.market_data import MarketData


# classes needed for serializing
class MetalWalletData(object):
    def __init__(self, name='silver', currency=None, metal_value=None, cash_spend=None, profit=None):
        self.name = name
        self.my_currency = currency
        self.metal_value = metal_value
        self.cash_spend = cash_spend
        self.profit = profit


class CashWalletData(object):
    def __init__(self, my_currency=None, cash=None):
        self.my_currency = my_currency
        self.cash = cash


class CryptoWalletData(object):
    def __init__(self, name='eth', currency=None, crypto_value=None, cash_spend=None, profit=None):
        self.name = name
        self.my_currency = currency
        self.crypto_value = crypto_value
        self.cash_spend = cash_spend
        self.profit = profit


class WalletData(object):
    def __init__(self, title=None, my_fortune=None):
        self.title = title
        self.my_fortune = my_fortune


class Wallet(object):
    """
    Wallet: class for calc asset value and profit.
    """
    def __init__(self, owner=None):
        self.owner = owner

    def get_metal_value(self, name, resource_id):
        value = Decimal(0)
        metal = Metal.objects.filter(owner=self.owner, name=name, id=resource_id).first()
        if metal:
            single_unit_value = MarketData.get_metal_market_price(name=name,
                                                                  unit=metal.unit,
                                                                  currency=self.owner.my_currency)
            value = single_unit_value * metal.amount
        return value.__round__(2)

    def get_metals_value(self, name):
        value = Decimal(0)
        for unit in Metal.UNIT_CHOICES:
            amount = Metal.objects.get_total_metal_amount(owner=self.owner, name=name, unit=unit[0])
            single_unit_value = MarketData.get_metal_market_price(name=name,
                                                                  unit=unit[0],
                                                                  currency=self.owner.my_currency)
            v = single_unit_value * amount
            value += v
        return value.__round__(2)

    def get_all_metals_value(self):
        value = Decimal(0)
        for name in Metal.METAL_CHOICES:
            v = self.get_metals_value(name=name[0])
            value += v
        return value.__round__(2)

    def get_metal_cash_spend(self, name, resource_id):
        metal = Metal.objects.filter(owner=self.owner, name=name, id=resource_id).first()
        return metal.bought_price.amount if metal else Decimal(0)

    def get_metals_cash_spend(self, name):
        result = Metal.objects.filter(owner=self.owner, name=name).aggregate(value=Sum('bought_price'))
        return result['value'] if result['value'] is not None else Decimal(0)

    def get_all_metals_cash_spend(self):
        result = Metal.objects.filter(owner=self.owner).aggregate(value=Sum('bought_price'))
        return result['value'] if result['value'] is not None else Decimal(0)

    def get_metal_profit(self, name, resource_id):
        return \
            self.get_metal_value(name=name, resource_id=resource_id) - \
            self.get_metal_cash_spend(name=name, resource_id=resource_id)

    def get_metals_profit(self, name):
        return self.get_metals_value(name=name) - self.get_metals_cash_spend(name=name)

    def get_all_metals_profit(self):
        return self.get_all_metals_value() - self.get_all_metals_cash_spend()

    def get_all_my_cash(self):
        return Cash.objects.get_total_cash(owner=self.owner)

    def get_crypto_value(self, name, resource_id):
        value = Decimal(0)
        crypto = Crypto.objects.filter(owner=self.owner, name=name, id=resource_id).first()
        if crypto:
            single_value = MarketData.get_crypto_market_price(name=name, currency=self.owner.my_currency)
            value = single_value * crypto.amount
        return value.__round__(2)

    def get_cryptos_value(self, name):
        amount = Crypto.objects.get_total_crypto_amount(owner=self.owner, name=name)
        single_value = MarketData.get_crypto_market_price(name=name, currency=self.owner.my_currency)
        value = single_value * amount
        return value.__round__(2)

    def get_all_cryptos_value(self):
        value = Decimal(0)
        for name in Crypto.CRYPTO_CHOICES:
            v = self.get_cryptos_value(name=name[0])
            value += v
        return value.__round__(2)

    def get_crypto_cash_spend(self, name, resource_id):
        crypto = Crypto.objects.filter(owner=self.owner, name=name, id=resource_id).first()
        return crypto.bought_price.amount if crypto else Decimal(0)

    def get_cryptos_cash_spend(self, name):
        result = Crypto.objects.filter(owner=self.owner, name=name).aggregate(value=Sum('bought_price'))
        return result['value'] if result['value'] is not None else Decimal(0)

    def get_all_cryptos_cash_spend(self):
        result = Crypto.objects.filter(owner=self.owner).aggregate(value=Sum('bought_price'))
        return result['value'] if result['value'] is not None else Decimal(0)

    def get_crypto_profit(self, name, resource_id):
        return \
            self.get_crypto_value(name=name, resource_id=resource_id) - \
            self.get_crypto_cash_spend(name=name, resource_id=resource_id)

    def get_cryptos_profit(self, name):
        return self.get_cryptos_value(name=name) - self.get_cryptos_cash_spend(name=name)

    def get_all_cryptos_profit(self):
        return self.get_all_cryptos_value() - self.get_all_cryptos_cash_spend()
