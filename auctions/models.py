from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from PIL import Image
import os
from django.core.files.images import get_image_dimensions

# 1️⃣ Custom User Model
class User(AbstractUser):
    
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True,  # Ensures no duplicate phone numbers
        help_text="Enter a valid phone number."
    )

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('bidder', 'Bidder'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='bidder')

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    # Fix related_name conflicts
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",
        blank=True,
    )

    def clean(self):
        """Ensure phone number is unique and enforce role for superusers."""
        if self.phone_number:
            self.phone_number = self.phone_number.replace(" ", "")  # Trim spaces

        if self.is_superuser and self.role != "admin":
            raise ValidationError("Superusers must have the role 'admin'.")

    def save(self, *args, **kwargs):
        """Override save method to clean data before saving."""
        self.full_clean()  # Runs clean() before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"

# 2️⃣ Vehicle Model
class Vehicle(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    mileage = models.IntegerField()
    condition = models.CharField(max_length=50, choices=[
        ('New', 'New'),
        ('Used', 'Used'),
        ('Damaged', 'Damaged'),
    ])
    description = models.TextField()
    images = models.ImageField(upload_to='vehicle_images/')
    videos = models.FileField(upload_to='vehicle_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

# 3️⃣ Auction Model
class Auction(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    vehicle = models.OneToOneField("Vehicle", on_delete=models.CASCADE)  # Assuming Vehicle exists
    title = models.CharField(max_length=255, blank=True)
    seller = models.ForeignKey("User", on_delete=models.CASCADE)  # Assuming User model exists
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_now_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to="auction_images/", default="auction_images/default.jpg")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Generate title if empty
        if not self.title and hasattr(self.vehicle, "make") and hasattr(self.vehicle, "model"):
            self.title = f"{self.vehicle.make} {self.vehicle.model} Auction"

        # Validate auction end time
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be later than start time.")

        super().save(*args, **kwargs)  # Save instance first

        # Resize image if it's too large
        if self.image and hasattr(self.image, "path") and os.path.exists(self.image.path):
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                img.thumbnail((800, 800))
                img.save(self.image.path)

    def __str__(self):
        if hasattr(self.vehicle, "make") and hasattr(self.vehicle, "model"):
            return f"Auction for {self.vehicle.make} {self.vehicle.model}"
        return f"Auction {self.id}"
    
# 4️⃣ Bid Model
class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} bid ksh {self.amount} on {self.auction.title}"

# 5️⃣ Payment Model
class Payment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"

# 6️⃣ Notification Model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"
    

#Vehicle Inspection Reports
class VehicleInspection(models.Model):
    auction = models.OneToOneField("Auction", on_delete=models.CASCADE)
    inspector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    inspection_date = models.DateField(auto_now_add=True)
    condition_summary = models.TextField()
    engine_status = models.CharField(max_length=50, choices=[("Good", "GOood"), ("Fair", "Fair"), ("Poor", "poor")])
    body_condition = models.CharField(max_length=50, choices=[("No Damage", "No Damage"), ("Minor Scratches", "Minor Scratches"), ("Dents", "Dents")])
    tire_condition = models.CharField(max_length=50, choices=[("New", "New"), ("Used - Good", "Used - Good"), ("Worn Out", "Worn Out")])
    interior_condition = models.TextField()
    additional_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Inspection Report for {self.auction.vehicle_title}"


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("seller", "Seller"),
        ("bidder", "Bidder"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="bidder")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.user.username


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[("Success", "Success"), ("Failed", "Failed")], default="Pending")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.user.username} - {self.transaction_id}"