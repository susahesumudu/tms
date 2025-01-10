from django.core.management.base import BaseCommand
from django.db.models import Count
from activities.models import Submission

class Command(BaseCommand):
    help = 'Remove duplicate submissions from the database'

    def handle(self, *args, **kwargs):
        # Find duplicates
        duplicates = (
            Submission.objects.values('student', 'exercise')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        # Remove duplicates
        for dup in duplicates:
            submissions = Submission.objects.filter(
                student=dup['student'], exercise=dup['exercise']
            ).order_by('id')  # Keep the first submission by ID

            # Skip the first submission and delete the rest
            for submission in submissions[1:]:
                submission.delete()

        self.stdout.write(self.style.SUCCESS('Duplicate submissions cleaned successfully!'))
