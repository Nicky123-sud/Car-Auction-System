from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Ensure a profile is created or updated when a User is saved."""
    if created:
        Profile.objects.create(user=instance)  # Create profile when a new user is created
    else:
        if hasattr(instance, "profile"):  # Check if the user has a profile before saving
            instance.profile.save()
