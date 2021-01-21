from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..market_data import MarketData
from resources.models import Crypto


metals = ['gold999', 'gold585', 'gold333', 'silver999', 'silver800']
units = ['oz', 'g', 'kg']
cryptos = [c[0] for c in Crypto.CRYPTO_CHOICES]


def is_metal_query_valid(name, unit):
    if not name in metals:
        return False
    if not unit in units:
        return False
    return True


def is_crypto_query_valid(name):
    if not name in cryptos:
        return False
    return True


@api_view(['GET'])
def market_metal(request):
    name = request.GET.get('name')
    unit = request.GET.get('unit')

    if is_metal_query_valid(name, unit):
        metal_price = MarketData.get_metal_market_price(name=name, unit=unit, currency=request.user.my_currency)
        data = {'name': name, 'unit': unit, 'price': metal_price.__round__(2), 'currency': request.user.my_currency}
    else:
        data = {'error': f"please provide following query for name: {', '.join(metals)} and unit: {', '.join(units)}"}
    return Response(data)


@api_view(['GET'])
def market_crypto(request):
    name = request.GET.get('name')

    if is_crypto_query_valid(name):
        crypto_price = MarketData.get_crypto_market_price(name=name, currency=request.user.my_currency)
        data = {'name': name, 'price': crypto_price, 'currency': request.user.my_currency}
    else:
        data = {'error': f"please provide following query for name: {', '.join(cryptos)}"}
    return Response(data)
