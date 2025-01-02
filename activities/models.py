from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

# Assuming Activity and Session models exist in courses.models
from courses.models import Activity, Session


class GradingRubric(models.Model):
    """
    Model representing a grading rubric with criteria, description, and maximum points.
    """
    criteria = models.CharField(max_length=255)
    description = models.TextField()
    max_points = models.FloatField()

    def __str__(self):
        return f"{self.criteria} ({self.max_points} points)"



class Exercise(models.Model):
    class DifficultyChoices(models.TextChoices):
        EASY = 'Easy', 'Easy'
        MEDIUM = 'Medium', 'Medium'
        HARD = 'Hard', 'Hard'

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=255)  # Title of the exercise
    description = models.TextField()  # Detailed description
    difficulty_level = models.CharField(max_length=50, choices=DifficultyChoices.choices)
    max_score = models.PositiveIntegerField()  # Maximum achievable score
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created

    def __str__(self):
        return self.title
    
    def clean(self):
        # Only validate if the instance has a primary key
        if self.pk:
            total_weight = sum(q.weighting for q in self.questions.all())
            if total_weight > 100:
                raise ValidationError("The total weight of questions in an exercise cannot exceed 100%.")



class Skill(models.Model):
    skill_name = models.CharField(max_length=255)  # Name of the skill
    skill_score = models.PositiveIntegerField()  # Score for the skill

    def __str__(self):
        return f"{self.skill_name} - Score: {self.skill_score}"


class Question(models.Model):
    skill = models.ManyToManyField(Skill, related_name='question_skills')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()  # Question text
    weighting = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)  # Weight of the question
    tutorial_url = models.URLField(blank=True, null=True)  # Optional tutorial URL
    video_url = models.URLField(blank=True, null=True)  # Optional video URL

    def __str__(self):
        return f"{self.text[:50]}... [Weight: {self.weighting}]"


class Submission(models.Model):
    class GradingRubric(models.TextChoices):
        BEGINNER = 'Beginner', 'Beginner'
        INTERMEDIATE = 'Intermediate', 'Intermediate'
        ADVANCED = 'Advanced', 'Advanced'

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user submitting the exercise
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)  # The related exercise
    submitted_file = models.FileField(upload_to='submissions/')  # The uploaded submission file
    self_efficacy_score = models.PositiveIntegerField(null=True, blank=True)  # Quick access
    score = models.PositiveIntegerField(null=True, blank=True)  # Grading score
    feedback = models.TextField(null=True, blank=True)  # Grading feedback
    grading_rubric = models.CharField(max_length=50, choices=GradingRubric.choices)  # Grading rubric selection
    graded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,blank=True,
        related_name='graded_submissions',
    )
    submitted_at = models.DateTimeField(auto_now_add=True)  # Timestamp when submission was made
    start_time = models.DateTimeField(null=True, blank=True)  # Start time for the submission
    end_time = models.DateTimeField(null=True, blank=True)  # End time for the submission
    duration = models.DurationField(null=True, blank=True)  # Total duration
    exercise_is_completed = models.BooleanField(default=False)  # Completion status
    is_ontime_completed = models.BooleanField(default=False)  # On-time submission status

    def start(self):
        self.start_time = now()
        self.end_time = None  # Reset end time
        self.duration = None  # Reset duration
        self.save()

    def stop(self):
        if self.start_time:
            self.end_time = now()
            self.duration = self.end_time - self.start_time
            self.exercise_is_completed = True  # Mark as completed
            if self.end_time <= self.exercise.created_at + timedelta(days=7):  # Example: 7-day deadline
                self.is_ontime_completed = True
            self.save()

    def time_remaining(self):
        if self.start_time and self.duration:
            end_time = self.start_time + self.duration
            remaining_time = end_time - now()
            return max(timedelta(0), remaining_time)  # Ensure no negative values
        return None

    def __str__(self):
        exercise_title = self.exercise.title if self.exercise else "Unknown Exercise"
        username = self.user.username if self.user else "Unknown User"
        return f"{username} - {exercise_title} (Completed: {self.exercise_is_completed})"


class Quiz(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255, verbose_name="Quiz Title")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    max_score = models.IntegerField(default=0, verbose_name="Total Score")

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(verbose_name="Question Text")
    weight = models.FloatField(default=1.0, verbose_name="Weight (%)")

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255, verbose_name="Choice Text")
    is_correct = models.BooleanField(default=False, verbose_name="Correct Answer")

    def __str__(self):
        return self.text


class QuizSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(null=True, blank=True)
    graded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_quiz_submissions'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    quiz_is_completed = models.BooleanField(default=False)
    is_ontime_completed = models.BooleanField(default=False)

    def stop(self):
        if self.start_time:
            self.end_time = now()
            self.duration = self.end_time - self.start_time
            self.quiz_is_completed = True
            if self.end_time <= self.quiz.created_at + timedelta(days=7):
                self.is_ontime_completed = True
            self.save()

    def __str__(self):
        quiz_title = self.quiz.title if self.quiz else "Unknown Quiz"
        username = self.user.username if self.user else "Unknown User"
        return f"{username} - {quiz_title} (Completed: {self.quiz_is_completed})"

    def stop(self):
        if not self.start_time:
            raise ValueError("Cannot stop the quiz. Start time is not set.")
        self.end_time = now()
        self.duration = self.end_time - self.start_time
        self.quiz_is_completed = True
        if self.end_time <= self.quiz.created_at + timedelta(days=7):
            self.is_ontime_completed = True
        self.save()


