import os
import json
import base64
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from utils.phone_number_formatter import format_phone_number
from utils.timestamp_evaluator import get_timestamp

CONSUMER_KEY = 'AbVyvUru4hhA195H5lZLlHJp4tqCEwLElIMu0ydPWxSmviC'
CONSUMER_SECRET = "PkIDUOPNNtBtZR1Ybh3Rh6d6GEoVKk4cRdtH8z4ZdYQUyrPlop1FpZExFhLBNjHz"


BASE_URL = "https://sandbox.safaricom.co.ke"
TOKEN_URL = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
STK_PUSH_URL = f"{BASE_URL}/mpesa/stkpush/v1/processrequest"

# Generate OAuth Token


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

# Initiate STK Push


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
            "CallBackURL": "https://truly-evident-hedgehog.ngrok-free.app/",
            "AccountReference": "RAPID RACK DISTRIBUTORS",
            "TransactionDesc": "Payment for goods",
        }

        response = requests.post(STK_PUSH_URL, headers=headers, json=payload)
        return JsonResponse(response.json())


mpesa_api_view = MpesaPayAPIView.as_view()


class PaymentCallBackAPIView(APIView):
    def post(self, request, *args, **kwargs):
        """We can provide a way to create logs of all transactions that has happened"""
        callback_data = request.body.decode("utf-8") or request.data

        print(callback_data)
        return JsonResponse({"message": "Callback received successfully"})


payment_callback = PaymentCallBackAPIView.as_view()
