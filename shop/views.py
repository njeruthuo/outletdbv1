from decimal import Decimal
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.transaction import atomic

from ext_apis.models import TransactionLog, TransactionStatusChoices
from shop.models import ShopStock, StockDisbursement, StockDisbursementStatuses
from stock.models import Product
from stock.serializers import StockSerializer
from stock.utils.disburse_stock import disburse_stock
from stock.utils.low_stock_alert import notify_admin_low_stock
from users.authentication import TokenAuthentication
from users.models import TextChoices, User
from .serializers import Shop, ShopSerializer, ShopStockSerializer, StockDisbursementSerializer


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

    def get_superuser(self):
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            print("No superuser found")
        return superuser

    @atomic
    def post(self, request, *args, **kwargs):

        shop_name = request.data.get('shop')
        product_name = request.data.get('product_name')
        disburseQuantity = request.data.get('disburseQuantity')

        if disburseQuantity and product_name and shop_name:
            # """Disburse stock to shop if all parameters are given"""
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

            return Response({'Disbursed': 'The product was disbursed successfully!'}, status=status.HTTP_200_OK)

        else:
            """Complete a sale if sale parameters are provided"""
            # Receive only the products and units sold, subtract from the shop's quantity, and make a log entry
            # products = request.data  # Assume this is a dictionary of product data
            user_shop = request.user.operated_shop.first()

            if not user_shop and not request.user.is_superuser:
                return Response({"error": "Shop not found for the user."}, status=status.HTTP_404_NOT_FOUND)

            if isinstance(request.data, str):
                import json
                products = json.loads(request.data)
            else:
                products = request.data

            if isinstance(products, dict):
                transaction_log = TransactionLog.objects.create(
                    user=request.user,
                    shop=user_shop,
                    receipt_ID=request.data.get("receipt_ID"),
                    transaction_status=TransactionStatusChoices.COMPLETED,
                    customer_number=request.data.get('payeeNumber'),
                    product_quantities={},
                    profit=0
                )

                for product_data in products.values():
                    if isinstance(product_data, dict):
                        try:
                            quantity_sold = product_data.get('quantity')
                            product_name = product_data['stock']['product']['name']

                            # Get the ShopStock instance
                            shop_stock = user_shop.shop_stocks.filter(
                                product__name=product_name).first()

                            if not shop_stock:
                                return Response({"error": f"Product '{product_name}' not found in shop."}, status=status.HTTP_404_NOT_FOUND)

                            # Check stock availability
                            if shop_stock.quantity < quantity_sold:
                                return Response({
                                    "error": f"Not enough stock for '{product_name}'. Available: {shop_stock.quantity}, Requested: {quantity_sold}"
                                }, status=status.HTTP_404_NOT_FOUND)

                            # Update stock levels
                            shop_stock.quantity -= quantity_sold
                            shop_stock.save()

                            # Update transaction log
                            transaction_log.products.add(shop_stock.product)
                            transaction_log.product_quantities[product_name] = quantity_sold
                            transaction_log.profit += (Decimal(shop_stock.product.product_buying_price) -
                                                       Decimal(shop_stock.product.price_per_item)) * quantity_sold

                            # Create a notification to the admin if stock levels fall below reorder level
                            if shop_stock.quantity <= shop_stock.reorder_level:
                                notify_admin_low_stock(
                                    shop=user_shop, sender=request.user, receiver=self.get_superuser())

                        except KeyError as e:
                            return Response({"error": f"Missing field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

                # Save the transaction log once
                transaction_log.save()

            return Response({"message": "Sale completed successfully."}, status=status.HTTP_200_OK)


shop_stock_mgt_api = ShopStockManagementAPI.as_view()


class ShopStockDisbursementAPIView(APIView):

    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_shop = user.operated_shop.first()

        if user.is_superuser:
            stock_disbursement = StockDisbursement.objects.all()
        else:
            stock_disbursement = StockDisbursement.objects.filter(
                shop=user_shop)

        completed_count = stock_disbursement.filter(
            status=StockDisbursementStatuses.DISBURSEMENT_RECEIVED).count()

        pending_count = stock_disbursement.filter(
            status=StockDisbursementStatuses.DISBURSED).count()

        return Response({'completed': completed_count, 'pending': pending_count}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


shop_stock_disbursement_api_view = ShopStockDisbursementAPIView.as_view()
