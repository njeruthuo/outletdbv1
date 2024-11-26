from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.transaction import atomic

from shop.models import ShopStock
from stock.models import Product
from stock.serializers import StockSerializer
from stock.utils import disburse_stock
from users.authentication import TokenAuthentication
from users.models import TextChoices
from .serializers import Shop, ShopSerializer


class ShopAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        if request.user.access_level==TextChoices.EMPLOYEE:
            user_shops = request.user.operated_shop.all()
            # Get stocks for all those shops
            all_shop_stocks = ShopStock.objects.filter(shop__in=user_shops)
            serialized_stock = StockSerializer(all_shop_stocks, many=True).data
            return Response(serialized_stock, status=status.HTTP_200_OK)

        elif request.user.access_level==TextChoices.ADMIN:
            shops = Shop.objects.all()
            shop_serializer = ShopSerializer(shops, many=True).data
            return Response(shop_serializer, status=status.HTTP_200_OK)
        
        elif request.user.access_level==TextChoices.MANAGER:
            """If the user is a manager, show all the shops in their region"""
            shops = Shop.objects.all() # filter per region
            shop_serializer = ShopSerializer(shops, many=True).data
            return Response(shop_serializer, status=status.HTTP_200_OK)
        
        else:
            return Response({'ACCESS DENIED':'THIS USER IS NOT PERMITTED!'}, status=status.HTTP_404_NOT_FOUND)

    @atomic
    def post(self, request, *args, **kwargs):
        # Combine request data and files into a single data dictionary
        data = request.data
        if 'licenses' in request.FILES:
            data['licenses'] = request.FILES['licenses']

        # Initialize the serializer with the combined data
        serializer = ShopSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Successfully created the shop"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @atomic
    def put(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_202_ACCEPTED)

    @atomic
    def delete(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


shop_api_view = ShopAPIView.as_view()


class ShopStockManagementAPI(APIView):
    @atomic
    def post(self, request, *args, **kwargs):
        print(request.data)

        shop_name = request.data.get('shop')
        product_name = request.data.get('product_name')
        disburseQuantity = request.data.get('disburseQuantity')

        try:
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            return Response({"Product Error": "Product Does Not Exist"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            shop = Shop.objects.get(branch_name=shop_name)
        except Shop.DoesNotExist:
            return Response({"Shop Error": "Shop Does Not Exist"}, status=status.HTTP_400_BAD_REQUEST)

        disburse_stock.disburse_stock(shop=shop, product=product,
                                      disburse_quantity=disburseQuantity)

        return Response({}, status=status.HTTP_201_CREATED)


shop_stock_mgt_api = ShopStockManagementAPI.as_view()
