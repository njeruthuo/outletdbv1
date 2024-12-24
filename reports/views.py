from users.authentication import TokenAuthentication
from ext_apis.serializers import TransactionLog, TransactionLogSerializer
from shop.serializers import StockDisbursement, StockDisbursementSerializer


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class ReportAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        qs = request.query_params.get('query')

        if not qs:
            return Response({'ERROR': f'QUERY CANNOT BE EMPTY'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user_shop = user.operated_shop.first()

        if qs == "Transactions":
            if user.is_superuser:
                transactions = TransactionLog.objects.all()
            else:
                transactions = TransactionLog.objects.filter(shop=user_shop)

            serializer = TransactionLogSerializer(transactions, many=True).data

            return Response(serializer, status=status.HTTP_200_OK)

        elif qs == "Disbursements":
            if user.is_superuser:
                disbursements = StockDisbursement.objects.all()
            else:
                disbursements = StockDisbursement.objects.filter(
                    shop=user_shop)

            serializer = StockDisbursementSerializer(
                disbursements, many=True).data

            return Response(serializer, status=status.HTTP_200_OK)

        elif qs == "Sales":
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({'ERROR': f'THE REPORT TYPE "{qs}" NOT AVAILABLE!'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


report_api_view = ReportAPIView.as_view()
