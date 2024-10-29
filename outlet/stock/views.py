from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from .serializers import StockSerializer, Stock


class StockAPIView(APIView):
    def get(self, request, *args, **kwargs):
        stock = Stock.objects.all()
        stock_serializer = StockSerializer(stock, many=True)
        return Response(stock_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data

        obj = {
            'product': {
                'name': data.get('name'),
                'price_per_item': float(data.get('price_per_item')),
                'category': data.get('category').replace(" ", ""),
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
                    'category': data.get('category').replace(" ", ""),
                    'brand': {'name': data.get('brand')},
                },
                'quantity': int(data.get('quantity')),
            }
            stock_serializer = StockSerializer(
                instance=stock_item, data=obj, partial=True)

            if stock_serializer.is_valid(raise_exception=True):
                stock_serializer.save()
                return Response({'message': 'Stock Item modified successfully'}, status=status.HTTP_200_OK)

        return Response({'message': 'Stock Item modified successfully'}, status=status.HTTP_400_BAD_REQUEST)


stock_api_view = StockAPIView.as_view()
