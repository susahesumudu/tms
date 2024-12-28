from django.db import models
from enrollments.models import Batch
from courses.models import Course, Module, Task
from center.models import Resource

# Abstract Base Class for Shared Fields
class PlanBase(models.Model):
    date_prepared = models.DateField()
    trade_subject = models.CharField(max_length=200)
    occupation = models.CharField(max_length=200)    
    date_revised = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

# Course Plan Model
class CoursePlan(PlanBase):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name="course_plan")
    coordinator_name = models.CharField(max_length=100)
    total_duration = models.PositiveIntegerField(help_text="Total duration of the course in hours")
    commencement_date = models.DateField()
    completion_date = models.DateField()
    overview = models.TextField(help_text="General overview or objectives of the course")

    def __str__(self):
        return f"Course Plan for {self.course.course_name}"

class CoursePlanModules(models.Model):
    course_plan = models.ForeignKey(CoursePlan, on_delete=models.CASCADE, related_name="modules")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="course_modules")
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Module {self.module.module_name} in {self.course_plan}"

# Training Plan Model
class TrainingPlan(PlanBase):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name="training_plan")
    training_plan_title = models.TextField(help_text="Details of the sessions in the plan")

    def __str__(self):
        return f"Training Plan for {self.course.course_name}"

class TrainingPlanModule(models.Model):
    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name="modules")    
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="training_modules")
    week_number = models.PositiveIntegerField()

    def __str__(self):
        return f"Module {self.module.module_name} - Week {self.week_number} in {self.training_plan}"

class TrainingPlanTask(models.Model):
    training_plan_module = models.ForeignKey(TrainingPlanModule, on_delete=models.CASCADE, related_name="tasks")    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="training_tasks")
    start_date = models.DateField()
    end_date = models.DateField() 

    def __str__(self):
        return f"Task {self.task.task_name} in {self.training_plan_module}"

# Weekly Plan Model
class WeeklyPlan(PlanBase):
    course_plan_module = models.ForeignKey(CoursePlanModules, on_delete=models.CASCADE, related_name="weekly_plans")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="weekly_plan_modules")

    def __str__(self):
        return f"Weekly Plan for {self.course_plan_module}"


class WeeklyTaskPlan(models.Model):
    weekly_plan = models.ForeignKey(WeeklyPlan, on_delete=models.CASCADE, related_name="tasks")  # Add ForeignKey to WeeklyPlan
    week_number = models.PositiveIntegerField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="weekly_tasks")
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Weekly Task Plan for Week {self.week_number} - Task {self.task.task_name}"


# Lesson Plan Model
class LessonPlan(PlanBase):
    course_plan_module = models.ForeignKey(CoursePlanModules, on_delete=models.CASCADE, related_name="lesson_plans")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lesson_modules")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="lesson_tasks")
    expected_date_commencement = models.DateField()
    actual_date_commencement = models.DateField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)
    machinery_tools = models.TextField(help_text="List of machinery, tools, and equipment required")
    instructional_material = models.TextField(help_text="List of instructional materials required")
    special_remarks = models.TextField(blank=True, null=True)
    topic_subject = models.CharField(max_length=200)
    total_duration = models.PositiveIntegerField(help_text="Duration in minutes")
    learning_objectives = models.TextField(help_text="Learning objectives for the session")
    teaching_activities = models.TextField(help_text="Trainer's activities during the session")
    learner_activities = models.TextField(help_text="Learner's activities during the session")
    resources_visuals = models.TextField(help_text="Resources and visuals required")
    assessment_activities = models.TextField()
    conclusion = models.TextField()
    trainer_signature = models.CharField(max_length=200)
    resources = models.ManyToManyField(Resource, related_name="lesson_resources")

    def __str__(self):
        return f"Lesson Plan for {self.module.module_name} - Task {self.task.task_name}"
