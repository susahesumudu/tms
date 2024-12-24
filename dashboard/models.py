from django.db import models

# Create your models here.

# dashboard/models.py

from django.db import models
from django.contrib.auth.models import User

class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard')
    # Example fields for a simple dashboard
    last_login_time = models.DateTimeField(blank=True, null=True)
    notifications_count = models.PositiveIntegerField(default=0)
    tasks_pending = models.PositiveIntegerField(default=0)
    tasks_completed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Dashboard"
