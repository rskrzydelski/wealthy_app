from rest_framework import serializers

from ..wallet import MetalWalletData, CashWalletData, CryptoWalletData, WalletData


class MetalWalletSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    my_currency = serializers.CharField(max_length=4)
    metal_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    cash_spend = serializers.DecimalField(max_digits=10, decimal_places=2)
    profit = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        return MetalWalletData(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.my_currency = validated_data.get('my_currency', instance.my_currency)
        instance.metal_value = validated_data.get('metal_value', instance.metal_value)
        instance.cash_spend = validated_data.get('cash_spend', instance.cash_spend)
        instance.profit = validated_data.get('profit', instance.profit)
        return instance


class CashWalletSerializer(serializers.Serializer):
    my_currency = serializers.CharField(max_length=4)
    cash = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        return CashWalletData(**validated_data)

    def update(self, instance, validated_data):
        instance.my_currency = validated_data.get('my_currency', instance.my_currency)
        instance.cash = validated_data.get('cash', instance.cash)


class CryptoWalletSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    my_currency = serializers.CharField(max_length=4)
    crypto_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    cash_spend = serializers.DecimalField(max_digits=10, decimal_places=2)
    profit = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        return CryptoWalletData(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.my_currency = validated_data.get('my_currency', instance.my_currency)
        instance.crypto_value = validated_data.get('crypto_value', instance.crypto_value)
        instance.cash_spend = validated_data.get('cash_spend', instance.cash_spend)
        instance.profit = validated_data.get('profit', instance.profit)
        return instance


class WalletSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    my_fortune = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        return WalletData(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.my_fortune = validated_data.get('my_fortune', instance.my_fortune)
        return instance
