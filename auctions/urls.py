from django.urls import path
from .views import (
    register, user_login, user_logout, dashboard, create_auction,
    auction_list, auction_detail, place_bid, seller_dashboard, seller_auctions,
    bidder_dashboard, edit_auction, delete_auction, admin_dashboard,
    add_user, update_user, delete_user, home, profile, search_vehicle, bid_history, notifications, quick_bid, mark_notification_read, initiate_payment, mpesa_callback
)

from django.shortcuts import redirect

# Redirect to login page if accessing `/accounts/login/`
def redirect_to_login(request):
    return redirect('/login/')

urlpatterns = [
    # General Pages
    path('', home, name='index'),
    path('accounts/login/', redirect_to_login),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # Dashboard Routes
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),
    path("dashboard/seller/", seller_dashboard, name="seller_dashboard"),
    path("dashboard/seller/auctions/", seller_auctions, name="seller_auctions"),  # ✅ Added this
    path("dashboard/bidder/", bidder_dashboard, name="bidder_dashboard"),
    path('notifications/', notifications, name='notifications'),
    path('bids/quick/', quick_bid, name='quick_bid'),

    # Auctions
    path("auctions/", auction_list, name="auction_list"),
    path("auctions/create/", create_auction, name="create_auction"),
    path("auctions/<int:auction_id>/", auction_detail, name="auction_detail"),
    path("auctions/<int:auction_id>/bid/", place_bid, name="place_bid"),
    path("auction/edit/<int:auction_id>/", edit_auction, name="edit_auction"),
    path("auction/delete/<int:auction_id>/", delete_auction, name="delete_auction"),
    path("search/", search_vehicle, name="search_vehicle"),
    path('bids/history/', bid_history, name='bid_history'),

    # Admin Management
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin/add-user/", add_user, name="add_user"),
    path("admin/update-user/<int:user_id>/", update_user, name="update_user"),
    path("admin/delete-user/<int:user_id>/", delete_user, name="delete_user"),
    
    path('notifications/', notifications, name='notifications'),
    path('notifications/mark-read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
    path("payment/", initiate_payment, name="initiate_payment"),
    path("payment/callback/", mpesa_callback, name="mpesa_callback"),
]
