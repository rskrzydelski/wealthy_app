from rest_framework.serializers import ModelSerializer, SerializerMethodField
from resources.models import Metal, Cash, Crypto


class MetalListSerializer(ModelSerializer):
    class Meta:
        model = Metal
        fields = [
            'owner',
            'id',
            'name',
            'amount',
            'unit',
            'bought_price',
            'bought_price_currency',
            'date_of_bought',
        ]


class MetalCreateSerializer(ModelSerializer):
    class Meta:
        model = Metal
        fields = [
            'owner',
            'name',
            'bought_price',
            'bought_price_currency',
            'amount',
            'unit',
            'date_of_bought',
            'description',
        ]


class MetalDetailSerializer(ModelSerializer):
    bought_price = SerializerMethodField('get_bought_price')

    class Meta:
        model = Metal
        fields = [
            'owner',
            'name',
            'bought_price',
            'bought_price_currency',
            'amount',
            'unit',
            'date_of_bought',
            'description',
        ]

    def get_bought_price(self, obj):
        return str(obj.bought_price)


class CashListSerializer(ModelSerializer):
    my_currency = SerializerMethodField('get_my_currency')

    class Meta:
        model = Cash
        fields = [
            'owner',
            'id',
            'my_currency',
            'save_date',
            'my_cash',
        ]

    def get_my_currency(self, obj):
        return str(obj.owner.my_currency)


class CashCreateSerializer(ModelSerializer):
    class Meta:
        model = Cash
        fields = [
            'owner',
            'save_date',
            'my_cash',
        ]


class CashDetailSerializer(ModelSerializer):
    class Meta:
        model = Cash
        fields = [
            'owner',
            'save_date',
            'my_cash',
        ]


class CryptoListSerializer(ModelSerializer):
    class Meta:
        model = Crypto
        fields = [
            'owner',
            'id',
            'name',
            'amount',
            'bought_price',
            'bought_price_currency',
            'date_of_bought',
        ]


class CryptoCreateSerializer(ModelSerializer):
    class Meta:
        model = Crypto
        fields = [
            'owner',
            'name',
            'bought_price',
            'bought_price_currency',
            'amount',
            'date_of_bought',
            'description',
        ]


class CryptoDetailSerializer(ModelSerializer):
    bought_price = SerializerMethodField('get_bought_price')

    class Meta:
        model = Crypto
        fields = [
            'owner',
            'name',
            'bought_price',
            'bought_price_currency',
            'amount',
            'date_of_bought',
            'description',
        ]

    def get_bought_price(self, obj):
        return str(obj.bought_price)
