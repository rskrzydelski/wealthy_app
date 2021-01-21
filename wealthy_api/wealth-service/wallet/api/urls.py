from django.urls import path, re_path
from . import views


app_name = 'wallet'
urlpatterns = [
    path('', views.wallet, name='wallet'),
    re_path(r'metals$', views.metal_wallet, name='metal-wallet'),
    re_path(r'metals/(?P<slug>[\w-]+)$', views.metal_wallet, name='metal-wallet'),
    re_path(r'metals/(?P<slug>[\w-]+)/(?P<resource_id>[^/]+)$', views.metal_wallet, name='metal-wallet'),
    re_path(r'cash$', views.cash_wallet, name='cash-wallet'),
    re_path(r'crypto$', views.crypto_wallet, name='crypto-wallet'),
    re_path(r'crypto/(?P<slug>[\w-]+)$', views.crypto_wallet, name='crypto-wallet'),
    re_path(r'crypto/(?P<slug>[\w-]+)/(?P<resource_id>[^/]+)$', views.crypto_wallet, name='crypto-wallet'),
]

