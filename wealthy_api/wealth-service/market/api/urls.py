from django.urls import path, re_path
from . import views


app_name = 'market'
urlpatterns = [
    re_path(r'metals$', views.market_metal, name='metal-market'),
    re_path(r'cryptos$', views.market_crypto, name='crypto-market'),
]

