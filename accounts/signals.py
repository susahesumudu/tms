from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Automatically create/update profiles based on user groups."""
    if created:
        if instance.groups.filter(name='Student').exists():
            StudentProfile.objects.create(user=instance)
        elif instance.groups.filter(name='Teacher').exists():
            TeacherProfile.objects.create(user=instance)
        elif instance.groups.filter(name='Staff').exists():
            StaffProfile.objects.create(user=instance)
        elif instance.groups.filter(name='Parent').exists():
            ParentProfile.objects.create(user=instance)
    else:
        # Update existing profiles
        profile_types = ['studentprofile', 'teacherprofile', 'staffprofile', 'parentprofile']
        for profile_type in profile_types:
            if hasattr(instance, profile_type):
                getattr(instance, profile_type).save()
