from django.db import models
from courses.models import Course, Module, Task , Activity 

class MainPlan(models.Model):
    name = models.CharField(max_length=200, unique=True)
    start_date = models.DateField(help_text="Start date of the plan.")
    end_date = models.DateField(help_text="End date of the plan.")
    no_weeks = models.PositiveIntegerField(help_text="Number of weeks in the plan.")
    no_days = models.PositiveIntegerField(help_text="Number of days in the plan.")
    no_sessions = models.PositiveIntegerField(help_text="Number of sessions in the plan.")
    no_theory_hrs = models.PositiveIntegerField(help_text="Number of theory hours in the plan.")
    no_practical_hrs = models.PositiveIntegerField(help_text="Number of practical hours in the plan.")

    def __str__(self):
        return f"Plan starting on {self.name}"

class LessonPlan(MainPlan):
    activity = models.ForeignKey(Activity, related_name='activity_plan', on_delete=models.CASCADE)
    no_minutes = models.PositiveIntegerField(help_text="Number of minutes allocated for the lesson.")

    def __str__(self):
        return f"Lesson Plan starting on {self.name}" 

class WeeklyPlan(MainPlan):
    task = models.ForeignKey(Task, related_name='task_paln', on_delete=models.CASCADE)
    lesson_plan = models.ForeignKey(LessonPlan, related_name='lessons_paln', on_delete=models.CASCADE)

    total_hours = models.PositiveIntegerField(help_text="Total hours allocated for the week.")
    total_minutes = models.PositiveIntegerField(help_text="Total minutes allocated for the week.")

    def __str__(self):
        return f"Weekly Plan starting on {self.name}" 

class TrainingPlan(MainPlan):
    module = models.ForeignKey(Module, related_name='modules_plan', on_delete=models.CASCADE)
    weekly_plan = models.ForeignKey(WeeklyPlan, related_name='weeklys_plan', on_delete=models.CASCADE)

    no_months = models.PositiveIntegerField(help_text="Number of months for the training plan.")

    def __str__(self):
        return f"Training Plan starting on {self.name}" 

class CoursePlan(MainPlan):
    course =  models.ForeignKey(Course, related_name='course_plan', on_delete=models.CASCADE)
    training_plan =  models.ForeignKey(TrainingPlan, related_name='trainings_plan', on_delete=models.CASCADE)
    no_months = models.PositiveIntegerField(help_text="Number of months for the course plan.")

    def __str__(self):
        return f"Course Plan starting on {self.name}"


