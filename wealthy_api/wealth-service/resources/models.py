from decimal import Decimal

from django.db import models
from django.db.models import Sum
from auth_app.models import InvestorUser

from djmoney.models.fields import MoneyField


# data model common for all resources
class Resource(models.Model):
    """
    Resource:
    Common data for metal and currency resource
    """
    owner = models.ForeignKey(InvestorUser, on_delete=models.CASCADE, default=1)
    bought_price = MoneyField(max_digits=10,
                              decimal_places=2,
                              default_currency='PLN')
    date_of_bought = models.DateField(auto_now_add=False)

    class Meta:
        abstract = True


class MetalManager(models.Manager):
    def get_metal_list(self, owner=None, name=None):
        """
        MetalManager:
        get_metal_list - returns list of particular metal or all metals
        :param name [silver, gold, none]
        :param owner
        :returns (Queryset) [silver list, gold list, all metals list]
        """
        if name:
            qs = super(MetalManager, self).filter(owner=owner, name=name)
        else:
            qs = super(MetalManager, self).filter(owner=owner)
        return qs

    def get_total_metal_amount(self, owner=None, name=None, unit='oz'):
        """
        MetalManager:
        get_total_metal_amount - returns total amount of particular metal
        :param name [silver, gold, none]
        :param owner
        :param unit [oz]
        :returns (Decimal) [silver amount, gold amount, None]
        """
        if name is None:
            return None

        amount = super(MetalManager, self).filter(owner=owner,
                                                  name=name,
                                                  unit=unit).aggregate(total_amount=Sum('amount'))
        return amount.get('total_amount') or Decimal(0)


# data model common for all metals
class Metal(Resource):
    """
    Metal:
    Precious metals data
    """
    objects = MetalManager()

    METAL_CHOICES = [
        ('silver999', 'Silver999'),
        ('silver800', 'Silver800'),
        ('gold999', 'Gold999'),
        ('gold585', 'Gold585'),
        ('gold333', 'Gold333'),
    ]
    UNIT_CHOICES = [
        ('oz', 'ounce'),
        ('g', 'gram'),
        ('kg', 'kilogram'),
    ]
    name = models.CharField(
        max_length=10,
        choices=METAL_CHOICES,
        default='silver999',
    )
    unit = models.CharField(max_length=10,
                            choices=UNIT_CHOICES,
                            default='oz')
    amount = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    description = models.TextField(blank=True, help_text='Type some information about this transaction (optional)')

    def __str__(self):
        return self.get_name_display()


class CashManager(models.Manager):
    def get_cash_list(self, owner=None):
        '''
        CashManager:
        get_cash_list - returns list my cash
        :param owner
        :returns (Queryset) [cash list]
        '''
        return super(CashManager, self).filter(owner=owner)

    def get_total_cash(self, owner=None):
        '''
        CashManager:
        get_total_cash - returns total amount of my cash
        :param owner
        :returns (Decimal) [my cash amount]
        '''
        total_cash = super(CashManager, self).filter(owner=owner).aggregate(my_cash=Sum('my_cash'))

        if total_cash['my_cash'] is None:
            value = Decimal(0)
        else:
            value = Decimal(total_cash['my_cash']).__round__(2)

        return value


class Cash(models.Model):
    """
    Cash:
    My cash
    """
    objects = CashManager()

    owner = models.ForeignKey(InvestorUser, on_delete=models.CASCADE, default=1)
    save_date = models.DateField(auto_now_add=False)
    my_cash = MoneyField(max_digits=10,
                         decimal_places=2,
                         null=True, blank=True,
                         default_currency='PLN')

    def __str__(self):
        return '{} cash {}'.format(self.owner.username, self.my_cash)


class CryptoManager(models.Manager):
    def get_crypto_list(self, owner=None, name=None):
        """
        CryptoManager:
        get_crypto_list - returns list of particular crypto or all crypto
        :param name [btc, bch, ..., none]
        :param owner
        :returns (Queryset) [btc list, bch list, ... , all crypto list]
        """
        if name:
            qs = super(CryptoManager, self).filter(owner=owner, name=name)
        else:
            qs = super(CryptoManager, self).filter(owner=owner)
        return qs

    def get_total_crypto_amount(self, owner=None, name=None):
        """
        CryptoManager:
        get_total_crypto_amount - returns total amount of particular crypto
        :param name [btc, bch, ..., none]
        :param owner
        :returns (Decimal) [btc amount, bch amount, ..., None]
        """
        if name is None:
            return None

        amount = super(CryptoManager, self).filter(owner=owner, name=name).aggregate(total_amount=Sum('amount'))
        return amount.get('total_amount') or Decimal(0)


class Crypto(Resource):
    """
    Crypto
    Cryptocurrencies data
    """
    objects = CryptoManager()

    CRYPTO_CHOICES = [
        ('btc', 'BTC'),
        ('bch', 'BCH'),
        ('eth', 'ETH'),
        ('xrp', 'XRP'),
        ('ltc', 'LTC'),
        ('dot', 'DOT'),
        ('neo', 'NEO'),
        ('flm', 'FLM'),
        ('theta', 'THETA'),
    ]
    name = models.CharField(
        max_length=10,
        choices=CRYPTO_CHOICES,
        default='eth',
    )
    amount = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    description = models.TextField(blank=True, help_text='Type some information about this transaction (optional)')

    def __str__(self):
        return f'{self.owner.username} crypto: '
