import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .utils import get_mpesa_access_token
from datetime import datetime

import base64



@csrf_exempt
def stk_push(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        amount = request.POST.get("amount")
        
        access_token = get_mpesa_access_token()
        
        if not access_token:
            return JsonResponse({"error": "Failed to get access token"}, status=400)
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode((settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode()).decode()
        
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "AccountReference": "Carvilla Auction System",
            "TransactionDesc": "Auction Payment"
        }
        
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        
        response = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)

        return JsonResponse(response.json())