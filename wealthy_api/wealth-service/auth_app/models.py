from django.db import models
from django.contrib.auth.models import AbstractUser


class InvestorUser(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    CURRENCY_CHOICES = [('USD', 'USD $'), ('EUR', 'EUR €'), ('PLN', 'PLN ZŁ'), ('CHF', 'CHF +')]
    my_currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='PLN')
    REQUIRED_FIELDS = ['username', 'my_currency']
    USERNAME_FIELD = 'email'

