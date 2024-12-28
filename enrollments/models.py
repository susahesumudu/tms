from datetime import timedelta
from django.contrib.auth.models import User, Group
from django.db import models
from courses.models import Course 

# Define Batch model
class Batch(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='batches')
    batch_code = models.CharField(max_length=50, unique=True)  # Batch number (unique)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # New fields to be added to the Batch model
    from_date = models.DateField()  # Start date of the course
    to_date = models.DateField(blank=True, null=True)  # End date of the course
    max_students = models.PositiveIntegerField()  # Max students per batch
    added_students = models.PositiveIntegerField(default=0)  # Added students, you may update this as needed
    lock_date = models.DateField(blank=True, null=True)  # Lock date for the batch


    # Define ManyToMany relationships with a related_name argument to avoid clashes
    students = models.ManyToManyField(User, related_name='batches_as_student', blank=True)
    teachers = models.ManyToManyField(User, related_name='batches_as_teacher', blank=True)

    def __str__(self):
        return f"{self.batch_code} ({self.from_date} - {self.to_date})"
    
    def save(self, *args, **kwargs):
        # Auto-calculate 'to_date' based on course duration
        if self.from_date and self.course and self.course.course_duration_months:
            self.to_date = self.from_date + timedelta(days=self.course.course_duration_months * 30)

        # Auto-calculate 'lock_date' as 75 days after 'from_date' if not provided
        if self.from_date and not self.lock_date:
            self.lock_date = self.from_date + timedelta(days=75)

        super().save(*args, **kwargs)

  


