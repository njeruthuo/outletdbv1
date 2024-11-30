from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.transaction import atomic

from shop.models import ShopStock
from stock.models import Product
from stock.serializers import StockSerializer
from stock.utils.disburse_stock import disburse_stock
from users.authentication import TokenAuthentication
from users.models import TextChoices
from .serializers import Shop, ShopSerializer


class ShopAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):

        shops = Shop.objects.all()  # filter per region
        shop_serializer = ShopSerializer(shops, many=True).data
        if shop_serializer:
            return Response(shop_serializer, status=status.HTTP_200_OK)

        return Response({'REQUEST ERROR': 'NO SHOPS FOUND!'}, status=status.HTTP_401_UNAUTHORIZED)

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
    authentication_classes = [TokenAuthentication]

    @atomic
    def post(self, request, *args, **kwargs):

        shop_name = request.data.get('shop')
        product_name = request.data.get('product_name')
        disburseQuantity = request.data.get('disburseQuantity')

        if disburseQuantity and product_name and shop_name:
            """Disburse stock to shop if all parameters are given"""
            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                return Response({"Product Error": "Product Does Not Exist"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                shop = Shop.objects.get(branch_name=shop_name)
            except Shop.DoesNotExist:
                return Response({"Shop Error": "Shop Does Not Exist"}, status=status.HTTP_400_BAD_REQUEST)

            disburse_stock(shop=shop, product=product,
                           disburse_quantity=disburseQuantity, disbursed_by=request.user)

            return Response({}, status=status.HTTP_201_CREATED)

        else:
            """Complete a sale if sale parameters are provided"""
            user_shop = request.user.operated_shop.first()

            if not user_shop:
                return Response({"error": "Shop not found for the user."}, status=status.HTTP_404_NOT_FOUND)

            # Receive only the products and units sold, subtract from the shop's quantity, and make a log entry
            products = request.data  # Assume this is a dictionary of product data

            if isinstance(products, dict):
                for product_data in products.values():
                    try:
                        quantity_sold = product_data['quantity']
                        product_name = product_data['stock']['product']['name']

                        # Get the ShopStock instance
                        shop_stock = user_shop.shop_stocks.filter(
                            product__name=product_name).first()

                        if not shop_stock:
                            return Response({"error": f"Product '{product_name}' not found in shop."}, status=status.HTTP_404_NOT_FOUND)

                        # Check if stock is sufficient
                        if shop_stock.quantity < quantity_sold:
                            return Response({
                                "error": f"Not enough stock for '{product_name}'. Available: {shop_stock.quantity}, Requested: {quantity_sold}"
                            }, status=status.HTTP_404_NOT_FOUND)

                        # Update stock levels
                        shop_stock.quantity -= quantity_sold
                        shop_stock.save()

                        # Log the sale (optional)
                        # SaleLog.objects.create(
                        #     shop=user_shop,
                        #     product=shop_stock.product,
                        #     quantity_sold=quantity_sold,
                        #     remaining_quantity=shop_stock.quantity
                        # )

                    except KeyError as e:
                        return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "Sale completed successfully."}, status=status.HTTP_200_OK)


shop_stock_mgt_api = ShopStockManagementAPI.as_view()
