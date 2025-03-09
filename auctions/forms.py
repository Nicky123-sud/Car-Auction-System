from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Auction, Bid, VehicleInspection

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True, help_text="Include country code (e.g., +254 712345678)")
    
    ROLE_CHOICES = [
        ("seller", "Seller"),
        ("bidder", "Bidder"),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "role", "password1", "password2"]
        
class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['vehicle', 'seller', 'start_time', 'end_time','starting_price', 'buy_now_price', 'image', 'status', 'description']
        
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        
        
class VehicleInspectionForm(forms.ModelForm):
    class Meta:
        model = VehicleInspection
        fields = ["condition_summary",
                  "engine_status",
                  "body_condition",
                  "tire_condition",
                  "interior_condition",
                  "additional_notes",
                  ]
        