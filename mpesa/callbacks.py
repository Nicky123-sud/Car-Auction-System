import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from auctions.models import Payment


@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body)
    result_code = data["Body"]["stkCallback"]["ResultCode"]
    
    if result_code == 0:
        # Payment was successfull
        amount = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
        phone = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]
        
        payment.objects.create(phone=phone, amount=amount, status="Completed")
        
        return JsonResponse({"message": "Payment received successfully"}, status=200)
    
    return JsonResponse({"error": "Payment failed"}, status=400)
