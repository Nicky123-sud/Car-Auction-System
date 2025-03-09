# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User, Vehicle, Auction, Bid, Payment, Notification, Auction, Bid, UserProfile, Payment

# # Custom User Admin
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     list_display = ("username", "email", "role", "is_staff", "is_active")
#     search_fields = ("username", "email", "role")
#     list_filter = ("role", "is_staff", "is_active")
    

# class AuctionAdmin(admin.ModelAdmin):
#     list_display = ("vehicle_title", "seller", "status", "created_at")
#     list_filter = ("status", "created_at")
#     search_fields = ("vehicle_title", "seller__username")
    
# class BidAdmin(admin.ModelAdmin):
#     list_display = ("auction", "bidder", "amount", "timestamp")
#     list_filter = ("timestamp")
#     search_fields = ("user__username", "phone_number")
    
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ("user", "phone_number", "role")
#     list_filter = ("role",)
#     search_fields = ("user__username", "phone_number")
   
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ("user", "auction", "amount", "status", "timestamp")
#     list_filter = ("status", "timestamp")
#     search_fields = ("user__username", "auction__vehicle_title")
    
# # Register Other Models
# admin.site.register(Vehicle)
# admin.site.register(Auction)
# admin.site.register(Bid)
# admin.site.register(Payment)
# admin.site.register(Notification)


# admin.site.register(Auction, AuctionAdmin)
# admin.site.register(Bid, BidAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(Payment, PaymentAdmin)




from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Vehicle, Auction, Bid, Payment, Notification, UserProfile

# Custom User Admin
# @admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active")
    search_fields = ("username", "email", "role")
    list_filter = ("role", "is_staff", "is_active")
    ordering = ("date_joined",)
    
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        
    )
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "is_active"),
        }),
    )
try:
    admin.site.register(User, CustomUserAdmin)
except admin.sites.AlreadyRegistered:
    pass
# admin.site.register(User, CustomUserAdmin)

# Auction Admin
@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "seller", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("vehicle__title", "seller__username")
    actions = ["approve_auctions", "reject_auctions"]
    
    def approve_auctions(self, request, queryset):
        queryset.update(status="approved")
    approve_auctions.short_description = "Approve selected auctions"
        
    def reject_auctions(self, request, queryset):
        queryset.update(status="rejected")
    reject_auctions.short_description = "Reject selected auctions"


# Bid Admin
@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ("auction", "bidder", "amount", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("bidder__username",)

# User Profile Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "role")
    list_filter = ("role",)
    search_fields = ("user__username", "phone_number")
    actions = ["make_admin", "make_seller", "make_bidder"]
    
    def make_admin(self, request, queryset):
        queryset.update(role="admin")
    make_admin.short_description = "Promote selected users to Admin"
    
    def make_seller(self, request, queryset):
        queryset.update(role="seller")
    make_seller.short_description = "Make selected users Sellers"
    
    def make_bidder(self, request, queryset):
        queryset.update(role="bidder")
    make_bidder.short_description = "Make selected users Bidders"

# Payment Admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "transaction_id", "amount", "status", "timestamp")  # ✅ Removed 'auction'
    search_fields = ("user__username", "transaction_id")
    list_filter = ("status", "timestamp")


# Register Other Models
admin.site.register(Vehicle)
admin.site.register(Notification)
