from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from ..models import InvestorUser


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = InvestorUser
        fields = [
            'id',
            'username',
            'email',
            'password',
            'my_currency',
        ]


