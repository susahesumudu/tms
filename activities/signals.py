from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Submission
from predictions.models import Prediction
from django.db.models import Sum

@receiver(post_save, sender=Submission)
@receiver(post_delete, sender=Submission)
def update_prediction_score(sender, instance, **kwargs):
    """
    Updates the assessment score in the Prediction model whenever a Submission is added, updated, or deleted.
    """
    # Get the student related to the submission
    student = instance.student

    # Calculate the total score from all submissions for the student
    total_score = Submission.objects.filter(student=student).aggregate(Sum('score'))['score__sum'] or 0

    # Update or create the corresponding Prediction object
    prediction, created = Prediction.objects.get_or_create(student=student)
    prediction.assessment_score = total_score
    prediction.save()
