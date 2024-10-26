from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import StockSerializer, Stock


class StockAPIView(APIView):
    def get(self, request, *args, **kwargs):
        stock = Stock.objects.all()
        stock_serializer = StockSerializer(stock, many=True)
        return Response(stock_serializer.data, status=status.HTTP_200_OK)


stock_api_view = StockAPIView.as_view()
