from django.db import models
from enrollments.models import Batch
from courses.models import Course, Module, Task, Session, Activity
from center.models import TrainingCenter, Resource

# Abstract Base Class for Shared Fields
class PlanBase(models.Model):
    date_prepared = models.DateField()
    
    class Meta:
        abstract = True  # Mark as an abstract base class

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
    course_plan = models.ForeignKey(CoursePlan,on_delete=models.CASCADE,related_name="course_plan_moduels")
    module = models.ForeignKey(Module,on_delete=models.CASCADE,related_name="course_plan_moduels_modules")
    start_date = models.DateField()
    end_date = models.DateField()


# Training Plan Model
class TrainingPlan(PlanBase):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="training_plans_module")
    occupation = models.CharField(max_length=200)
    date_revised = models.DateField(blank=True, null=True)
    week_number = models.PositiveIntegerField()
    session_info = models.TextField(help_text="Details of the sessions in the plan")
    tasks_to_cover = models.TextField()
    special_services = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Training Plan for Module {self.module.module_name} - Week {self.week_number}"

# Weekly Plan Model
class WeeklyPlan(PlanBase):
    course_plan = models.ForeignKey(CoursePlan, on_delete=models.CASCADE, related_name="weekly_plans_course_plan")
    week_number = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    modules_covered = models.ManyToManyField(Module, related_name="weekly_plans_modules")
    tasks_to_cover = models.TextField(help_text="List of tasks or objectives for the week")
    activities = models.TextField(help_text="Details about activities to be conducted during the week")
    assessment_schedule = models.TextField(help_text="Planned assessments for the week")

    def __str__(self):
        return f"Week {self.week_number} Plan for {self.course_plan.course.course_name}"

# Lesson Plan Model
class LessonPlan(PlanBase):
    trade_subject = models.CharField(max_length=200)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lesson_plans_module")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="lesson_plans_task")
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
    resources = models.ManyToManyField(Resource, related_name="training_plans_resources")


    def __str__(self):
        return f"Lesson Plan for {self.module.module_name} - Task {self.task.task_name}"
