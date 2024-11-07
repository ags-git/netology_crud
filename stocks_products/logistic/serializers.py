from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'description']

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']


    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = Stock.objects.create(**validated_data)

        for position in positions:
            StockProduct.objects.create(stock=stock,
                                        product=position.pop('product'),
                                        quantity=position.pop('quantity'),
                                        price=position.pop('price'))
        return stock


    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        instance.address = validated_data.get('address', instance.address)
        instance.save()

        StockProduct.objects.filter(stock=instance).delete()

        for position in positions:
            StockProduct.objects.create(stock=instance,
                                        product=position.pop('product'),
                                        quantity=position.pop('quantity'),
                                        price=position.pop('price'))
        return instance
