from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .serializers import (
    MetalListSerializer,
    MetalCreateSerializer,
    MetalDetailSerializer,
    CashListSerializer,
    CashCreateSerializer,
    CashDetailSerializer,
    CryptoListSerializer,
    CryptoCreateSerializer,
    CryptoDetailSerializer,
)
from resources.models import Metal, Cash, Crypto


class MetalLstCreateAPIView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MetalListSerializer
        else:
            return MetalCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # collect query strings
        query_name = self.request.GET.get('name')
        if query_name:
            queryset = Metal.objects.filter(owner=self.request.user, name=query_name)
        else:
            queryset = Metal.objects.filter(owner=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)


class MetalDetailDelUpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = MetalDetailSerializer

    def get_queryset(self):
        queryset = Metal.objects.filter(owner=self.request.user)
        return queryset


class CashLstCreateAPIView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CashListSerializer
        else:
            return CashCreateSerializer

    def get_queryset(self):
        queryset = Cash.objects.get_cash_list(owner=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, my_cash_currency=self.request.user.my_currency)


class CashDetailUpdateDelAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CashDetailSerializer

    def get_queryset(self):
        queryset = Cash.objects.filter(owner=self.request.user)
        return queryset


class CryptoLstCreateAPIView(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CryptoListSerializer
        else:
            return CryptoCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # collect query strings
        query_name = self.request.GET.get('name')
        if query_name:
            queryset = Crypto.objects.filter(owner=self.request.user, name=query_name)
        else:
            queryset = Crypto.objects.filter(owner=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)


class CryptoDetailDelUpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CryptoDetailSerializer

    def get_queryset(self):
        queryset = Crypto.objects.filter(owner=self.request.user)
        return queryset
