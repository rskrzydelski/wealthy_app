from decimal import Decimal
from mongomarket import mongomarket_tools


class MarketData(object):
    def __init__(self):
        pass

    @staticmethod
    def get_metal_market_price(name, unit, currency):
        doc = mongomarket_tools.get_metal_price(name, unit, currency)
        if not doc:
            return Decimal(0)
        return Decimal(doc.get('value')) if doc.get('value') is not None else Decimal(0)

    @staticmethod
    def get_crypto_market_price(name, currency):
        doc = mongomarket_tools.get_crypto_price(name, currency)
        if not doc:
            return Decimal(0)
        return Decimal(doc.get('value')) if doc.get('value') is not None else Decimal(0)
