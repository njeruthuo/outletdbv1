from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

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


stock_api_view = StockAPIView.as_view()
