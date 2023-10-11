from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import UserProfile, Account

@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile()
        user_profile.user_id = instance.id
        user_profile.profile_picture = "photos/default/default_user_profile_img.png"
        user_profile.save()