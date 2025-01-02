from django.db import models
from django.contrib.auth.models import User  # Assuming you're using Django's built-in User model
from django.utils import timezone  # for timezone handling
from courses.models import  Activity,Session


from django.contrib.auth.models import User

class CommonEfficacyQuestion(models.Model):
    question_text = models.CharField(max_length=255)  # The efficacy question
    is_active = models.BooleanField(default=True)     # Whether the question is active

    def __str__(self):
        return self.question_text



class GradingRubric(models.Model):
    criteria = models.CharField(max_length=255)  # The criteria being graded
    description = models.TextField()  # Description of the criteria
    max_points = models.FloatField()  # Maximum points for this criteria
    points_awarded = models.FloatField(null=True, blank=True)  # Points awarded for this criteria

    def __str__(self):
        return f"{self.criteria} ({self.max_points} points)"


class MainActivity(models.Model):
    ACTIVITY_TYPES = [
        ('Exercise', 'Exercise'),
        ('Assignment', 'Assignment'),
        ('Project', 'Project'),
        ('Demonstration', 'Demonstration'),
        ('Lecture', 'Lecture'),
        ('Group', 'Group'),
    ]
    

    MODE_TYPES = [
        ('Online', 'Online'),
        ('Video', 'Video'),
        ('Physical', 'Physical'),
    ]
    activity = models.ForeignKey(Activity, related_name='activity_activity', on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=100)
    activity_code = models.CharField(max_length=10)
    description = models.TextField()
    session = models.ForeignKey(Session, related_name='activity_session', on_delete=models.CASCADE)
    mode = models.CharField(max_length=10, choices=MODE_TYPES)
    minutes = models.FloatField()  # Hours required for this activity (could be practical or theoretical hours)
    #publish_grading_rubric = models.BooleanField(default=False)  # Option to publish rubric
    deadline = models.DateTimeField()  # Deadline for submission
    efficacy_questions = models.ManyToManyField(CommonEfficacyQuestion, blank=True)

    def __str__(self):
        return self.tself.activity_name


class LearningActivity(MainActivity):
    """Model for Learning-related activities, extending Activity."""
    learning_goal = models.TextField()  # The learning goal or outcome for the activity
    is_required = models.BooleanField(default=True)  # Whether this learning activity is required or optional

    def __str__(self):
        return f"Learning Activity: {self.activity_name}"


class PracticingActivity(MainActivity):
    """Model for Practicing-related activities, extending Activity."""
    practice_type = models.CharField(max_length=100)  # E.g., Individual, Group, etc.
    is_assessment_related = models.BooleanField(default=False)  # Whether this practice is linked to assessments

    def __str__(self):
        return f"Practicing Activity: {self.activity_name}"


class AssessmentActivity(MainActivity):

    ASSESSMENT_TYPES = [
        ('MCQ', 'MCQ'),
        ('Presentation', 'Presentation'),
        ('Project', 'Project'),
        ('Demonstration', 'Demonstration'),
        ('Assingment', 'Assingment'),
      
    ]
    """Model for assessment-related activities, extending Activity."""
    assessment_type = models.CharField(max_length=100,choices=ASSESSMENT_TYPES)  # E.g., Quiz, Test, Final Project
    max_marks = models.FloatField()  # Maximum marks for the assessment

    def __str__(self):
        return f"Assessment Activity: {self.activity_name}"


class Submission(models.Model):
    activity = models.ForeignKey(Activity, related_name='submissions', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='submissions', on_delete=models.CASCADE)  # Assuming User model
    submission_file = models.FileField(upload_to='submissions/')  # File upload
    submitted_at = models.DateTimeField(auto_now_add=True)  # Automatically set to now when submitted
    marks = models.FloatField(null=True, blank=True)  # Marks can be assigned later
    feedback = models.TextField(null=True, blank=True)  # Optional feedback for the submission
    end_time = models.DateTimeField(null=True, blank=True)  # Ensure end_time is set if relevant
    on_time_completion = models.BooleanField(default=False)  # Tracks whether it was submitted on time
    marks_awarded = models.FloatField(default=0.0)

    def duration(self):
        if self.end_time and self.submitted_at:
            return (self.end_time - self.submitted_at).total_seconds() / 3600  # Duration in hours
        return 0.0  # Return 0 if end_time or submitted_at is None

    def is_achieved_on_time(self):
        now = timezone.now()
        if now > self.activity.submission_deadline:
            self.on_time_completion = False
            return 'Late'
        elif now < self.activity.submission_deadline:
            self.on_time_completion = True
            return 'Earlier'
        else:
            self.on_time_completion = True
            return 'On Time'

    def is_late(self):
        if self.submitted_at > self.activity.submission_deadline:
            self.on_time_completion = False
            return True
        self.on_time_completion = True
        return False

    def __str__(self):
        return f"Submission by {self.student.username} for {self.activity.activity_name}"



class MarksTracker(models.Model):
    students = models.ForeignKey(
        User,on_delete=models.CASCADE,
        related_name='student',
        limit_choices_to={'groups__name': 'Student'},
        blank=True
    )

    daily_marks = models.FloatField(default=0.0)
    weekly_marks = models.FloatField(default=0.0)
    monthly_marks = models.FloatField(default=0.0)
    course_wise_marks = models.FloatField(default=0.0)
    final_grade = models.CharField(max_length=10)
    final_assessment_score = models.FloatField(null=True, blank=True)  # Allow null if it's computed later
    tasks_completed = models.IntegerField(default=0)
    exercises_completed = models.IntegerField(default=0)
    on_time_completion = models.BooleanField(default=False)
    practical_hours = models.FloatField(default=0.0)
    theory_hours = models.FloatField(default=0.0)
    num_of_prev_attempts = models.IntegerField(default=0)
    industry_training_experience = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.student.username}'s Marks"


