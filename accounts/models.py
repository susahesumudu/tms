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
    """Fields specific to students, including profile and performance tracking."""
    # Profile Details
    final_grade = models.CharField(max_length=50, blank=True, null=True)  # Final grade of the student
    certificate_no = models.CharField(max_length=100, blank=True, null=True)
    is_certificate_issued = models.BooleanField(default=False)
    is_payment_completed = models.BooleanField(default=False)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    # Academic and Task Details
    final_marks = models.PositiveIntegerField(blank=True, null=True)
    module_marks = models.PositiveIntegerField(blank=True, null=True)
    task_marks = models.PositiveIntegerField(blank=True, null=True)
    completed_total_mod = models.PositiveIntegerField(blank=True, null=True)
    completed_total_task = models.PositiveIntegerField(blank=True, null=True)
    completed_total_activity = models.PositiveIntegerField(blank=True, null=True)
    is_completed_total_tasks = models.BooleanField(default=False)

    # Performance Metrics
    daily_marks = models.FloatField(default=0.0)
    weekly_marks = models.FloatField(default=0.0)
    monthly_marks = models.FloatField(default=0.0)
    course_wise_marks = models.FloatField(default=0.0)
    final_assessment_score = models.FloatField(blank=True, null=True)
    tasks_completed = models.PositiveIntegerField(default=0)
    exercises_completed = models.PositiveIntegerField(default=0)
    on_time_completion = models.BooleanField(default=False)
    practical_hours = models.FloatField(default=0.0)
    theory_hours = models.FloatField(default=0.0)
    num_of_prev_attempts = models.PositiveIntegerField(default=0)
    industry_experience = models.PositiveIntegerField(blank=True, null=True)
    industry_training_experience = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username}'s Profile"



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

from courses.models import Activity
from activities.models import Exercise

class ClickLog(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True, related_name='click_log_activity')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True, blank=True, related_name='click_log_exercise')
    url = models.URLField()  # URL of the page where the click occurred
    element_id = models.CharField(max_length=255, null=True, blank=True)  # ID of the clicked element
    element_tag = models.CharField(max_length=50, null=True, blank=True)  # HTML tag of the clicked element
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)  # Logged-in user
    timestamp = models.DateTimeField(auto_now_add=True)  # Time of the click
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # User's IP address
    user_agent = models.TextField(null=True, blank=True)  # Browser info for analytics

    def __str__(self):
        return f"Click on {self.element_id or self.element_tag} at {self.timestamp}"

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['activity']),
        ]