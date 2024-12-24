from django.db import models
from django.contrib.auth.models import User

class BaseProfile(models.Model):
    """
    Common fields shared by all profiles.
    This is an abstract model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.username} Profile"


class StudentProfile(BaseProfile):
    """Fields specific to students."""
    final_grade = models.CharField(max_length=50, blank=True, null=True)
    certificate_no = models.CharField(max_length=100, blank=True, null=True)
    is_certificate_issued = models.BooleanField(default=False)
    is_payment_completed = models.BooleanField(default=False)
    final_marks = models.PositiveIntegerField(blank=True, null=True)
    module_marks = models.PositiveIntegerField(blank=True, null=True)
    task_marks = models.PositiveIntegerField(blank=True, null=True)
    completed_total_mod = models.PositiveIntegerField(blank=True, null=True)
    completed_total_task = models.PositiveIntegerField(blank=True, null=True)
    completed_total_activity = models.PositiveIntegerField(blank=True, null=True)
    is_completed_total_tasks = models.BooleanField(default=False)
    industry_experience = models.PositiveIntegerField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)


class TeacherProfile(BaseProfile):
    """Fields specific to teachers."""
    subject_specialty = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class StaffProfile(BaseProfile):
    """Fields specific to staff."""
    department = models.CharField(max_length=100, blank=True, null=True)


class ParentProfile(BaseProfile):
    """Fields specific to parents."""
    children_count = models.PositiveIntegerField(blank=True, null=True)
    students = models.ManyToManyField(
        User,
        related_name='parents',
        limit_choices_to={'groups__name': 'Student'},
        blank=True
    )
