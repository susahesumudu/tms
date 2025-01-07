from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User  # Import the User model

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

from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import ClickLog
from activities.models import StudentActivityLog
from django.utils.text import slugify

@receiver(post_save, sender=ClickLog)
def update_student_activity_log(sender, instance, **kwargs):
    activity_code = instance.activity.code if instance.activity else 'UNKNOWN'
    exercise_code = instance.exercise.code if instance.exercise else 'UNKNOWN'
    id_student = instance.user.id if instance.user else 0
    id_site = hash(instance.url)
    date = instance.timestamp.date().toordinal()
    sum_click = 1

    slug = slugify(f"{activity_code}-{exercise_code}-{id_student}-{date}")

    student_log, created = StudentActivityLog.objects.update_or_create(
        slug=slug,
        defaults={
            'activity_code': activity_code,
            'exercise_code': exercise_code,
            'id_student': id_student,
            'id_site': id_site,
            'date': date,
            'sum_click': sum_click,
        }
    )

    if not created:
        student_log.sum_click += 1
        student_log.save()
