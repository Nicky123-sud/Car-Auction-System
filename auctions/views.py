from django.shortcuts import render, redirect, get_object_or_404
from users.decorators import role_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from .models import User, Auction, Bid, VehicleInspection, Vehicle
from .forms import AuctionForm, BidForm, VehicleInspectionForm
from .utils import fetch_vehicle_history


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


@role_required(["bidder"])
def bidder_dashboard(request):
    return render(request, "auctions/bidder_dashboard.html")


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
