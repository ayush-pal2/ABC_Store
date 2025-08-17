from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from accounts.models import Profile, Customer, Vendor

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        if profile.user_type == 'C':
            Customer.objects.get_or_create(user=instance)
        elif profile.user_type == 'V':
            Vendor.objects.get_or_create(user=instance)

@receiver(post_save, sender=Profile)
def create_associated_model(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'C':
            Customer.objects.get_or_create(user=instance.user)
        elif instance.user_type == 'V':
            Vendor.objects.get_or_create(user=instance.user)
