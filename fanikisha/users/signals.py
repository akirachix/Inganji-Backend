# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import UserProfile

# @receiver(post_save, sender=UserProfile)
# def create_user_profile(sender, instance, created, **kwargs):
#     """Create a User when a new User is created."""
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=UserProfile)
# def save_user_profile(sender, instance, **kwargs):
#     """Save the User when the User is saved."""
#     instance.profile.save()
