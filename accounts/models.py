from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

# Automatically create or update the Profile when a User is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a Profile instance when a new User is created
        Profile.objects.create(user=instance)
    else:
        # Save the Profile instance when an existing User is updated
        if hasattr(instance, 'profile'):  # Ensure the Profile exists
            instance.profile.save()

