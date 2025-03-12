from django.shortcuts import render, redirect, get_object_or_404
from users.decorators import role_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from .models import User, Auction, Bid, VehicleInspection, Vehicle, Notification
from .forms import UserRegisterForm, AuctionForm, BidForm, VehicleInspectionForm
from .utils import fetch_vehicle_history
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json  # ✅ Correct standard Python import
import re  # ✅ Correct standard Python import
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from .models import Payment
import base64
import datetime
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import base64
import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# ------------------ User Authentication ------------------ #

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get("role")

            if role == "admin":
                messages.error(request, "You cannot register as an admin.")
                return redirect("register")

            user.role = role
            user.save()
            login(request, user)
            messages.success(request, f"Account created successfully as a {role}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = UserRegisterForm()

    return render(request, "auctions/register.html", {"form": form})



def user_login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "auctions/login.html")


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    if user.role == "admin":
        return redirect("admin_dashboard")
    elif user.role == "seller":
        return redirect("seller_dashboard")
    elif user.role == "bidder":
        return redirect("bidder_dashboard")
    else:
        messages.error(request, "Invalid role. Contact support.")
        return redirect('login')


# ------------------ Admin Dashboard & User Management ------------------ #

def is_admin(user):
    return user.is_authenticated and user.role == "admin"


@staff_member_required
def admin_dashboard(request):
    users = User.objects.exclude(role="admin")  # Get only sellers & bidders
    total_users = users.count()
    total_auctions = Auction.objects.count()
    pending_auctions = Auction.objects.filter(status="pending").count()
    total_bids = Bid.objects.count()

    return render(request, "auctions/admin_dashboard.html", {
        "users": users,
        "total_users": total_users,
        "total_auctions": total_auctions,
        "pending_auctions": pending_auctions,
        "total_bids": total_bids,
    })


@login_required
@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        role = request.POST["role"]

        if role not in ["seller", "bidder"]:  # Validate role selection
            messages.error(request, "Invalid role selected.")
            return redirect("admin_dashboard")

        password = make_password("defaultpassword")  # Assign a default password
        User.objects.create(username=username, email=email, role=role, password=password)
        messages.success(request, "User added successfully!")

    return redirect("admin_dashboard")


@login_required
@user_passes_test(is_admin)
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        new_role = request.POST.get("role")

        if new_role in ["seller", "bidder"]:
            user.role = new_role
            user.save()
            messages.success(request, "User role updated successfully!")
        else:
            messages.error(request, "Invalid role selection.")

    return redirect("admin_dashboard")


@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.role != "admin":  # Prevent deleting an admin
        user.delete()
        messages.success(request, "User deleted successfully.")
    else:
        messages.error(request, "Cannot delete an admin user.")

    return redirect("admin_dashboard")


# ------------------ Seller & Bidder Dashboards ------------------ #

@role_required(["seller"])
def seller_dashboard(request):
    auctions = Auction.objects.filter(seller=request.user)
    return render(request, "auctions/seller_dashboard.html", {"auctions": auctions})


@login_required
def bidder_dashboard(request):
    pending_payments = Payment.objects.filter(user=request.user, status="Pending")

    context = {
        "pending_payments": pending_payments.exists(),
    }
    return render(request, "auctions/bidder.html", context)


# ------------------ Auction Management ------------------ #

@login_required
def create_auction(request):
    if request.method == "POST":
        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.seller = request.user
            auction.current_price = auction.starting_price
            auction.save()
            messages.success(request, "Auction created successfully!")
            return redirect('auction_list')
    else:
        form = AuctionForm()

    return render(request, "auctions/create_auction.html", {'form': form})

@login_required
def auction_list(request):
    auctions = Auction.objects.filter(is_active=True, status="approved").order_by('-start_time')
    return render(request, "auctions/auction_list.html", {'auctions': auctions})

@login_required
def auction_detail(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    vehicle_history = fetch_vehicle_history(auction.vin) if auction.vin else None

    return render(request, "auctions/auction_detail.html", {"auction": auction, "vehicle_history": vehicle_history})

@login_required
def edit_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id, seller=request.user)

    if request.method == "POST":
        form = AuctionForm(request.POST, request.FILES, instance=auction)
        if form.is_valid():
            form.save()
            messages.success(request, "Auction updated successfully!")
            return redirect("seller_dashboard")
    else:
        form = AuctionForm(instance=auction)

    return render(request, "auctions/edit_auction.html", {"form": form, "auction": auction})

@login_required
def delete_auction(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id, seller=request.user)

    if request.method == "POST":
        auction.delete()
        messages.success(request, "Auction deleted successfully.")
        return redirect("seller_dashboard")

    return render(request, "auctions/delete_auction.html", {"auction": auction})


@login_required
def place_bid(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)

    if not auction.is_active or auction.status != "approved":
        messages.error(request, "This auction is not available for bidding.")
        return redirect("auction_detail", auction_id=auction.id)

    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data["amount"]

            if bid_amount <= auction.current_price:
                messages.error(request, "Your bid must be higher than the current price.")
                return redirect("auction_detail", auction_id=auction.id)

            bid = form.save(commit=False)
            bid.bidder = request.user
            bid.auction = auction
            bid.save()

            auction.current_price = bid_amount
            auction.save()

            messages.success(request, "Bid placed successfully!")
            return redirect("auction_detail", auction_id=auction.id)
    else:
        form = BidForm()

    return render(request, "auctions/place_bid.html", {'auction': auction, 'form': form})


# ------------------ Profile & Homepage ------------------ #

def profile(request):
    return render(request, 'auctions/profile.html')


def home(request):
    # Fetch the latest 3 active auctions that have images
    featured_auctions = Auction.objects.filter(status="active").exclude(image="auction_images/default.jpg").order_by('-start_time')[:3]

    return render(request, "auctions/index.html", {"featured_auctions": featured_auctions})



def search_vehicle(request):
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    year = request.GET.get('year')

    vehicles = Vehicle.objects.all()

    if query:
        vehicles = vehicles.filter(title__icontains=query) | vehicles.filter(make__icontains=query) | vehicles.filter(model__icontains=query)
    if min_price:
        vehicles = vehicles.filter(price__gte=min_price)
    if max_price:
        vehicles = vehicles.filter(price__lte=max_price)
    if year:
        vehicles = vehicles.filter(year=year)

    # Get unique years for filtering dropdown
    years = Vehicle.objects.values_list('year', flat=True).distinct().order_by('-year')

    return render(request, 'auctions/search_vehicle.html', {'vehicles': vehicles, 'years': years})

@login_required
def bid_history(request):
    # Use bidder instead of user
    bids_list = Bid.objects.filter(bidder=request.user).select_related('auction__vehicle').order_by('-timestamp')

    # Paginate Results (10 bids per page)
    paginator = Paginator(bids_list, 10)
    page_number = request.GET.get('page')
    bids = paginator.get_page(page_number)

    # Get unique years for filtering dropdown
    years = Vehicle.objects.values_list('year', flat=True).distinct().order_by('-year')

    context = {
        'bids': bids,
        'years': years,
    }
    return render(request, 'auctions/bid_history.html', context)


@login_required
def notifications(request):
    # Fetch user notifications (ordered by newest first)
    user_notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')

    # Paginate results (10 notifications per page)
    paginator = Paginator(user_notifications, 10)
    page_number = request.GET.get('page')
    notifications_page = paginator.get_page(page_number)

    context = {
        'notifications': notifications_page,
        'unread_notifications_count': user_notifications.filter(read_status=False).count(),
    }
    return render(request, 'auctions/notifications.html', context)


@login_required
def mark_notification_read(request, notification_id):
    if request.method == "POST":
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.read_status = True
        notification.save()
        return JsonResponse({"status": "success", "message": "Notification marked as read"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)



@csrf_exempt
@login_required
def quick_bid(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = data.get('amount')
            auction_id = data.get('auction_id')
            
            auction = Auction.objects.get(id=auction_id)
            
            #Create a new bid
            new_bid = Bid.objects.create(user=request.user, auction=auction, amount=amount)
            
            return JsonResponse({'message': 'Bid placed successfully!', 'bid_id': new_bid.id}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def initiate_payment(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        amount = request.POST.get("amount")

        # Generate Lipa Na M-Pesa Online Shortcode and Password
        business_short_code = settings.MPESA_BUSINESS_SHORTCODE
        passkey = settings.MPESA_PASSKEY
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(f"{business_short_code}{passkey}{timestamp}".encode()).decode()

        # M-Pesa API Endpoint
        access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

        # Get M-Pesa Access Token
        access_token_response = requests.get(access_token_url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
        access_token = access_token_response.json().get("access_token")

        # STK Push Request
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        payload = {
            "BusinessShortCode": business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": business_short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "AccountReference": "CarAuction",
            "TransactionDesc": "Payment for Car Auction"
        }

        response = requests.post(stk_push_url, json=payload, headers=headers)
        response_data = response.json()

        # Save Payment Record
        if response_data.get("ResponseCode") == "0":
            Payment.objects.create(
                user=request.user,
                transaction_id=response_data["CheckoutRequestID"],
                phone_number=phone_number,
                amount=amount,
                status="Pending"
            )
            return JsonResponse({"message": "Payment initiated successfully. Check your phone to complete the payment."})
        else:
            return JsonResponse({"error": "Payment initiation failed"}, status=400)
    return render(request, "auctions/payment.html")

@csrf_exempt
def mpesa_callback(request):
    if request.method == "POST":
        data = request.body.decode("utf-8")
        response_data = json.loads(data)
        
        checkout_request_id = response_data["Body"]["stkCallback"]["CheckoutRequestID"]
        result_code = response_data["Body"]["stkCallback"]["ResultCode"]
        
        
        # Get Payment Record
        payment = Payment.objects.filter(transaction_id=checkout_request_id).first()
        if payment:
            if result_code == 0:
                payment.status = "Completed"
            else:
                payment.status = "Failed"
            payment.save()

        return JsonResponse({"message": "Payment status updated successfully."})
    return JsonResponse({"error": "Invalid request"}, status=400)



def seller_auctions(request):
    # Fetch and display seller's auctions
    return render(request, 'auctions/seller_auctions.html')
