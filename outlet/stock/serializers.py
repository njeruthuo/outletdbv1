from rest_framework import serializers

from .models import Stock, Product, Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name',
                  #   'contact'
                  ]


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = ['name', 'price_per_item', 'brand', 'category']

    def create(self, validated_data):

        brand_data = validated_data.pop('brand')

        brand = {'name': brand_data.get('name')}

        brand_serializer = BrandSerializer(data=brand)
        if brand_serializer.is_valid(raise_exception=True):
            brand_instance = brand_serializer.save()

        product = Product.objects.create(
            brand=brand_instance, **validated_data)
        return product


class StockSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Stock
        fields = ['product', 'quantity', 'last_updated']

    def create(self, validated_data):

        product_data = validated_data.pop('product')
        product = {
            'name': product_data.get('name'),
            'price_per_item': int(product_data.get('price_per_item')),
            'category': product_data.get('category').replace(" ", ""),
            'brand': {'name': product_data.get('brand')['name']}
        }

        product_serializer = ProductSerializer(data=product)
        if product_serializer.is_valid(raise_exception=True):
            product_instance = product_serializer.save()

        stock = Stock.objects.create(
            product=product_instance, **validated_data)
        return stock

        # return super().create(validated_data)
