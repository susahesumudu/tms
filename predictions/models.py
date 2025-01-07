import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Prediction(models.Model):
    code = models.CharField(max_length=10, unique=True, blank=True)  # Allow blank to auto-generate
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
    slug = models.SlugField(unique=True, max_length=100, blank=True)  # Allow blank to auto-generate

    def save(self, *args, **kwargs):
        # Auto-generate unique code if not set
        if not self.code:
            self.code = str(uuid.uuid4())[:8]  # Shorten UUID to fit max_length=10
        # Auto-generate slug if not set
        if not self.slug:
            self.slug = slugify(self.code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Prediction for {self.student.username} by {self.predicted_by.username}"
