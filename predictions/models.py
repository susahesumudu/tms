from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MarksTracker(models.Model):
    #student = models.ForeignKey(User, on_delete=models.CASCADE)
    daily_marks = models.FloatField(default=0.0)
    weekly_marks = models.FloatField(default=0.0)
    monthly_marks = models.FloatField(default=0.0)
    course_wise_marks = models.FloatField(default=0.0)
    final_grade = models.CharField(max_length=10)
    final_assessment_score = models.FloatField()
    tasks_completed = models.IntegerField()
    exercises_completed = models.IntegerField()
    on_time_completion = models.BooleanField()
    practical_hours = models.FloatField()
    theory_hours = models.FloatField()
    num_of_prev_attempts = models.IntegerField()
    industry_training_experience = models.FloatField()

    def __str__(self):
        # Use 'username', 'first_name', or 'last_name' instead of 'name'
        return f"{self.student.username}'s Marks"
