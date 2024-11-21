import base64
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from utils.timestamp_evaluator import get_timestamp

# Safaricom API credentials
CONSUMER_KEY = 'HIB8zBKPlrl8WOusIf0KEunJV0nAKAJqjMnYLsADxCOezsn5'
CONSUMER_SECRET = 'AnFd51KaKDfzFHDwPsKH2FSe9AUSN2FrUEkkmsNRsjbClgjagFxAtYNguBevswDR'

# M-Pesa API URLs
# Change to production URL when live
BASE_URL = "https://sandbox.safaricom.co.ke"
TOKEN_URL = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
STK_PUSH_URL = f"{BASE_URL}/mpesa/stkpush/v1/processrequest"

# Generate OAuth Token


def get_access_token():
    credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {"Authorization": f"Basic {encoded_credentials}"}
    response = requests.get(TOKEN_URL, headers=headers)
    return response.json().get("access_token")

# Initiate STK Push


def format_phone_number(args):
    str_input = str(args)
    if str_input.startswith("254"):
        return str_input
    if len(str_input) == 10 and str_input.startswith("0"):
        return str_input.replace("0", "254")


class MpesaPayAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        phone_number = format_phone_number(data.get(
            "phone_number"))  # Customer's phone number
        amount = data.get("amount")  # Payment amount

        print(phone_number)

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
            "CallBackURL": "https://yourdomain.com/callback",
            "AccountReference": "Test Payment",
            "TransactionDesc": "Payment for goods",
        }

        response = requests.post(STK_PUSH_URL, headers=headers, json=payload)
        return JsonResponse(response.json())


mpesa_api_view = MpesaPayAPIView.as_view()


@csrf_exempt
def initiate_payment(request):
    if request.method == "POST":
        print(request.data)
        data = request.POST
        phone_number = format_phone_number(data.get(
            "phone_number"))  # Customer's phone number
        amount = data.get("amount")  # Payment amount

        print(phone_number)

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
            "CallBackURL": "https://yourdomain.com/callback",
            "AccountReference": "Test Payment",
            "TransactionDesc": "Payment for goods",
        }

        response = requests.post(STK_PUSH_URL, headers=headers, json=payload)
        return JsonResponse(response.json())


def generate_password():
    timestamp = get_timestamp()
    short_code = "174379"  # Test short code
    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2b5c4f57c192b36bdfef5ac2b1aa3d83"
    data_to_encode = f"{short_code}{passkey}{timestamp}"
    return base64.b64encode(data_to_encode.encode()).decode()


@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        callback_data = request.body.decode("utf-8")
        # Handle and save the callback data
        print(callback_data)
        return JsonResponse({"message": "Callback received successfully"})
