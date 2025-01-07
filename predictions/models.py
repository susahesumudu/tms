from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

class Prediction(models.Model):
    student = models.ForeignKey(User, related_name="student_predictions", on_delete=models.CASCADE)
    predicted_by = models.ForeignKey(User, related_name="teacher_predictions", on_delete=models.CASCADE)
    assessment_score = models.FloatField()
    industry_training_experience = models.FloatField()
    average_time_per_task = models.FloatField()
    completed_no_activity = models.FloatField()
    total_task_completed = models.FloatField()
    self_efficacy_score = models.FloatField()
    practicals_hrs = models.FloatField()
    theory_hrs = models.FloatField()
    predicted_grade = models.CharField(max_length=10, null=True, blank=True)
    prediction_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Prediction for {self.student.username} by {self.predicted_by.username}"
