import json
import base64
import logging
import requests

from django.views import View
from django.http import JsonResponse
from django.db.models.functions import TruncMonth

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from rest_framework import status
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response

from ext_apis.models import TransactionLog
from ext_apis.serializers import TransactionLogSerializer
from users.authentication import TokenAuthentication
from utils.timestamp_evaluator import get_timestamp
from utils.phone_number_formatter import format_phone_number

CONSUMER_KEY = 'AbVyvUru4hhA195H5lZLlHJp4tqCEwLElIMu0ydPWxSmviC'
CONSUMER_SECRET = "PkIDUOPNNtBtZR1Ybh3Rh6d6GEoVKk4cRdtH8z4ZdYQUyrPlop1FpZExFhLBNjHz"


BASE_URL = "https://sandbox.safaricom.co.ke"
TOKEN_URL = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
STK_PUSH_URL = f"{BASE_URL}/mpesa/stkpush/v1/processrequest"


def get_access_token():
    response = requests.request("GET", 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', headers={
                                'Authorization': 'Basic c0FiVnl2VXJ1NGhoQTE5NUg1bFpMbEhKcDR0cUNFd0xFbElNdTB5ZFBXeFNtdmlDOlBrSURVT1BOTnRCdFpSMVliaDNSaDZkNkdFb1ZLazRjUmR0SDh6NFpkWVFVeXJQbG9wMUZwWkV4RmhMQk5qSHo='})
    data = json.loads(response.text.encode('utf8'))['access_token']
    return data


def generate_password():
    timestamp = get_timestamp()
    short_code = "174379"  # Test short code
    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    data_to_encode = f"{short_code}{passkey}{timestamp}"
    return base64.b64encode(data_to_encode.encode()).decode()


class MpesaPayAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        phone_number = format_phone_number(data.get(
            "phone_number"))  # Customer's phone number
        amount = data.get("amount")  # Payment amount

        token = get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "BusinessShortCode": "174379",  # Test short code
            "Password": generate_password(),
            "Timestamp": get_timestamp(),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": "174379",
            "PhoneNumber": phone_number,
            "CallBackURL": "https://truly-evident-hedgehog.ngrok-free.app/api/external/callback/",
            "AccountReference": "RAPID RACK DISTRIBUTORS",
            "TransactionDesc": "Payment for goods",
        }

        response = requests.post(STK_PUSH_URL, headers=headers, json=payload)
        return JsonResponse(response.json())


mpesa_api_view = MpesaPayAPIView.as_view()


logger = logging.getLogger(__name__)


class PaymentCallBackAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            callback_data = json.loads(request.body.decode("utf-8"))

            # Extract receipt ID and transaction details
            stk_callback = callback_data.get("Body", {}).get("stkCallback", {})
            receipt_id = stk_callback.get("CheckoutRequestID")
            result_code = stk_callback.get("ResultCode")
            result_desc = stk_callback.get("ResultDesc")

            if not receipt_id:
                logger.error("Missing receipt ID in callback data")
                return JsonResponse({"ResultCode": 1, "ResultDesc": "Missing receipt ID"}, status=400)

            logger.info(f"Callback data received: {callback_data}")

            # Notify the static WebSocket group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "transaction_updates",
                {
                    "type": "transaction_update",
                    "status": "SUCCESS" if result_code == 0 else "FAILED",
                    "receipt_id": receipt_id,
                    "description": result_desc,
                }
            )

            # Respond to M-Pesa
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Callback received successfully"})

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON received: {str(e)}")
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid JSON format"}, status=400)

        except Exception as e:
            logger.error(f"Error processing callback: {str(e)}")
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Internal server error"}, status=500)


payment_callback = PaymentCallBackAPIView.as_view()


class TransactionLogsAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_superuser:
            monthly_counts = (
                TransactionLog.objects.annotate(
                    month=TruncMonth('date_created'))
                .values('month')
                .annotate(count=Count('id'))
            )
        else:
            user_shop = user.operated_shop.first()
            monthly_counts = (
                TransactionLog.objects.filter(shop=user_shop).annotate(
                    month=TruncMonth('date_created'))
                .values('month')
                .annotate(count=Count('id'))
            )
        log_counts_by_month = {
            record['month'].strftime('%b'): record['count']
            for record in monthly_counts
        }

        return Response(log_counts_by_month, status=status.HTTP_200_OK)


transaction_logs_api_view = TransactionLogsAPIView.as_view()
