from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from shop.models import ShopStock
from users.models import TextChoices
from users.authentication import TokenAuthentication


class StockAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):

        search = request.GET.get('search')
        if search:
            stock = Stock.objects.filter(
                Q(product__category__name__icontains=search) |
                Q(product__name__icontains=search) |
                Q(product__brand__name__icontains=search)
            )
        else:
            """If the user making the request is an employee, return a list of products in their shop"""
            if request.user.access_level == TextChoices.EMPLOYEE:
                user_shops = request.user.operated_shop.all()
                all_shop_stocks = ShopStock.objects.filter(shop__in=user_shops)
                serialized_stock = StockSerializer(
                    all_shop_stocks, many=True).data
                return Response(serialized_stock, status=status.HTTP_200_OK)
            else:
                stock = Stock.objects.all()

        stock_serializer = StockSerializer(stock, many=True)
        return Response(stock_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data

        obj = {
            'product': {
                'name': data.get('name'),
                'price_per_item': float(data.get('price_per_item')),
                'category': {
                    'name': data.get('category'),
                },
                'brand': {'name': data.get('brand')},
            },
            'quantity': int(data.get('quantity')),
        }

        serializer = StockSerializer(data=obj)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'message': 'Stock Item added successfully'}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        stock_item = get_object_or_404(Stock, id=pk)

        if stock_item:
            data = request.data
            obj = {
                'product': {
                    'name': data.get('name'),
                    'price_per_item': float(data.get('price_per_item')),
                    'category': {
                        'name': data.get('category'),
                    },
                    'brand': {'name': data.get('brand')},
                },
                'quantity': int(data.get('quantity')),
            }
            stock_serializer = StockSerializer(
                instance=stock_item, data=obj, partial=True)

            if stock_serializer.is_valid(raise_exception=True):
                stock_serializer.save()
                return Response({'message': 'Stock Item modified successfully'}, status=status.HTTP_200_OK)

        return Response({'message': 'Stock Item modification failed'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            Stock.objects.filter(id=pk).delete()
            return Response({'message': 'Stock Item delete successful'}, status=status.HTTP_200_OK)
        return Response({'message': 'Stock Item deletion failed'}, status=status.HTTP_400_BAD_REQUEST)


stock_api_view = StockAPIView.as_view()


class CategoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data, status=status.HTTP_200_OK)


category_api_view = CategoryAPIView.as_view()


class BrandAPIView(APIView):
    def get(self, request, *args, **kwargs):
        brands = Brand.objects.all()
        brand_serializer = BrandSerializer(brands, many=True)
        return Response(brand_serializer.data, status=status.HTTP_200_OK)


brand_api_view = BrandAPIView.as_view()


