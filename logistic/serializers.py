from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    # product = serializers.PrimaryKeyRelatedField(
    #     queryset=Product.objects.all(),
    #     required=True,
    # )
    # quantity = serializers.IntegerField(min_value=1, default=1)
    # price = serializers.IntegerField(min_value=1)

    class Meta:
        model = StockProduct
        fields = ['id', 'stock', 'product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['id', 'address', 'products']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        # заполняем связанные таблицы
        for position in positions:
            StockProduct.objects.create(stock=position['stock'], product=position['product'],
                                        quantity=position['quantity'], price=position['price'])

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # обновляем связанные таблицы
        for position in positions:
            StockProduct.objects.update_or_create(stock=position['stock'], product=position['product'],
                                                  defaults={'quantity': position['quantity'], 'price': position['price']})

        return stock
