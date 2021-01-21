from decimal import Decimal
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import MetalWalletSerializer, CryptoWalletSerializer, CashWalletSerializer, WalletSerializer
from ..wallet import Wallet, MetalWalletData, CryptoWalletData, CashWalletData, WalletData
from resources.models import Metal, Crypto


def validate_metal_slug_name(slug):
    if any(slug == m[0] for m in Metal.METAL_CHOICES):
        return True
    else:
        return False


def validate_crypto_slug_name(slug):
    if any(slug == m[0] for m in Crypto.CRYPTO_CHOICES):
        return True
    else:
        return False


def get_metal_wallet(wallet_inst, currency, name, resource_id):
    data = {}
    data['metal_value'] = wallet_inst.get_metal_value(name=name, resource_id=resource_id)
    data['cash_spend'] = wallet_inst.get_metal_cash_spend(name=name, resource_id=resource_id)
    data['name'] = f'Metal {name} with id {resource_id}'
    data['currency'] = currency
    data['profit'] = wallet_inst.get_metal_profit(name=name, resource_id=resource_id)
    return data


def get_metals_wallet(wallet_inst, currency, name):
    data = {}
    data['metal_value'] = wallet_inst.get_metals_value(name=name)
    data['cash_spend'] = wallet_inst.get_metals_cash_spend(name=name)
    if validate_metal_slug_name(name):
        data['name'] = f'All {name}'
    else:
        pass
    data['currency'] = currency
    data['profit'] = wallet_inst.get_metals_profit(name)
    return data


def get_all_metals_wallet(wallet_inst, currency):
    data = {}
    data['metal_value'] = wallet_inst.get_all_metals_value()
    data['cash_spend'] = wallet_inst.get_all_metals_cash_spend()
    data['name'] = 'All metals'
    data['currency'] = currency
    data['profit'] = wallet_inst.get_all_metals_profit()
    return data


def get_crypto_wallet(wallet_inst, currency, name, resource_id):
    data = {}
    data['crypto_value'] = wallet_inst.get_crypto_value(name=name, resource_id=resource_id)
    data['cash_spend'] = wallet_inst.get_crypto_cash_spend(name=name, resource_id=resource_id)
    data['name'] = f'Crypto {name} with id {resource_id}'
    data['currency'] = currency
    data['profit'] = wallet_inst.get_crypto_profit(name=name, resource_id=resource_id)
    return data


def get_cryptos_wallet(wallet_inst, currency, name):
    data = {}
    data['crypto_value'] = wallet_inst.get_cryptos_value(name=name)
    data['cash_spend'] = wallet_inst.get_cryptos_cash_spend(name=name)
    if validate_crypto_slug_name(name):
        data['name'] = f'All {name}'
    else:
        pass
    data['currency'] = currency
    data['profit'] = wallet_inst.get_cryptos_profit(name)
    return data


def get_all_cryptos_wallet(wallet_inst, currency):
    data = {}
    data['crypto_value'] = wallet_inst.get_all_cryptos_value()
    data['cash_spend'] = wallet_inst.get_all_cryptos_cash_spend()
    data['name'] = 'All cryptocurrencies'
    data['currency'] = currency
    data['profit'] = wallet_inst.get_all_cryptos_profit()
    return data


@api_view(['GET'])
def metal_wallet(request, slug=None, resource_id=None):
    wallet = Wallet(owner=request.user)

    if slug and resource_id:
        data = get_metal_wallet(wallet_inst=wallet, currency=request.user.my_currency, name=slug, resource_id=resource_id)
    elif slug:
        data = get_metals_wallet(wallet_inst=wallet, currency=request.user.my_currency, name=slug)
    else:
        data = get_all_metals_wallet(wallet_inst=wallet, currency=request.user.my_currency)

    instance = MetalWalletData(**data)
    serializer = MetalWalletSerializer(instance)
    return Response(serializer.data)


@api_view(['GET'])
def crypto_wallet(request, slug=None, resource_id=None):
    wallet = Wallet(owner=request.user)

    if slug and resource_id:
        data = get_crypto_wallet(wallet_inst=wallet, currency=request.user.my_currency, name=slug, resource_id=resource_id)
    elif slug:
        data = get_cryptos_wallet(wallet_inst=wallet, currency=request.user.my_currency, name=slug)
    else:
        data = get_all_cryptos_wallet(wallet_inst=wallet, currency=request.user.my_currency)

    instance = CryptoWalletData(**data)
    serializer = CryptoWalletSerializer(instance)
    return Response(serializer.data)


@api_view(['GET'])
def cash_wallet(request):
    wallet = Wallet(owner=request.user)
    my_cash = wallet.get_all_my_cash()
    instance = CashWalletData(my_currency=request.user.my_currency, cash=my_cash)
    serializer = CashWalletSerializer(instance)
    return Response(serializer.data)


@api_view(['GET'])
def wallet(request):
    title = 'Summary of all assets value'
    wallet = Wallet(owner=request.user)

    metal_value = wallet.get_all_metals_value()
    my_cash = wallet.get_all_my_cash()
    crypto_value = wallet.get_all_cryptos_value()

    my_fortune = metal_value + my_cash + crypto_value
    if metal_value is None or crypto_value is None:
        title = "Market data is not available"
        my_fortune = Decimal(0)
    instance = WalletData(title=title, my_fortune=my_fortune)
    serializer = WalletSerializer(instance)
    return Response(serializer.data)
