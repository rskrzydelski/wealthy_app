from django.urls import re_path
from . import views


app_name = 'resources'
urlpatterns = [
    re_path(r'metals$', views.MetalLstCreateAPIView.as_view(), name='res-create-lst'),
    re_path(r'metals/(?P<pk>\d+)$', views.MetalDetailDelUpdateAPIView.as_view(), name='res-detail'),
    re_path(r'cash$', views.CashLstCreateAPIView.as_view(), name='cash-create-lst'),
    re_path(r'cash/(?P<pk>\d+)$', views.CashDetailUpdateDelAPIView.as_view(), name='cash-detail'),
    re_path(r'crypto$', views.CryptoLstCreateAPIView.as_view(), name='cr-create-lst'),
    re_path(r'crypto/(?P<pk>\d+)$', views.CryptoDetailDelUpdateAPIView.as_view(), name='cr-detail'),
]
