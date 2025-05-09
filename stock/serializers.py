from rest_framework import serializers

from .models import Stock, Product, Brand, Category


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name',
                  'contact'
                  ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price_per_item', 'brand', 'category']

    def create(self, validated_data):

        brand_data = validated_data.pop('brand')
        category_data = validated_data.pop('category')

        brand = Brand.objects.get(name=brand_data.get('name'))
        category = Category.objects.get(name=category_data.get('name'))

        product = Product.objects.create(
            brand=brand, category=category, **validated_data)
        return product

    def update(self, instance, validated_data):
        # Extract nested brand and category data
        brand_data = validated_data.pop('brand', None)
        category_data = validated_data.pop('category', None)

        # Update or create brand instance if brand data is provided
        if brand_data:
            brand_instance, created = Brand.objects.get_or_create(
                name=brand_data.get('name')
            )
            instance.brand = brand_instance

        # Update or create category instance if category data is provided
        if category_data:
            category_instance, created = Category.objects.get_or_create(
                name=category_data.get('name')
            )
            instance.category = category_instance

        # Update other fields in the product instance
        return super().update(instance, validated_data)


class StockSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Stock
        fields = ['id', 'product', 'quantity', 'last_updated']

    def create(self, validated_data):

        product_data = validated_data.pop('product')
        product = {
            'name': product_data.get('name'),
            'price_per_item': int(product_data.get('price_per_item')),
            'category': product_data.get('category'),
            'brand': {'name': product_data.get('brand')['name']}
        }

        product_serializer = ProductSerializer(data=product)
        if product_serializer.is_valid(raise_exception=True):
            product_instance = product_serializer.save()

        stock = Stock.objects.create(
            product=product_instance, **validated_data)
        return stock

    def update(self, instance, validated_data):
        product_data = validated_data.pop('product')
        product = {
            'name': product_data.get('name'),
            'price_per_item': int(product_data.get('price_per_item')),
            'category': product_data.get('category'),
            'brand': {'name': product_data.get('brand')['name']}
        }

        product_serializer = ProductSerializer(
            instance=instance.product, data=product, partial=True)
        if product_serializer.is_valid(raise_exception=True):
            product_serializer.save()

        return super().update(instance, validated_data)
