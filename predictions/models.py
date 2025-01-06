from django.db import models
from django.contrib.auth.models import User

from django.db import models



# # Resource Model
# class Resource(models.Model):
#     resource_id = models.CharField(max_length=50, unique=True)
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True, null=True)
#     uploaded_date = models.DateField()

#     def __str__(self):
#         return self.name




# # Interaction Model
# class Interaction(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Student'})    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     date = models.DateField()
#     click_count = models.PositiveIntegerField()

#     def __str__(self):
#         return f"{self.student.name} - {self.resource.name} on {self.date}"


# from django.db import models

# # Trainees Model
# class Trainee(models.Model):
#     trainee_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     age = models.PositiveIntegerField()
#     gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
#     education_level = models.CharField(max_length=100)
#     prior_experience = models.PositiveIntegerField(default=0)
#     self_efficacy_score = models.PositiveIntegerField()

#     def __str__(self):
#         return self.name

# # Attendance Model
# class Attendance(models.Model):
#     attendance_id = models.AutoField(primary_key=True)
#     trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
#     date = models.DateField()
#     session_type = models.CharField(max_length=50, choices=[('Theory', 'Theory'), ('Practical', 'Practical')])
#     status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

# # Engagement Model
# class Engagement(models.Model):
#     engagement_id = models.AutoField(primary_key=True)
#     trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
#     week_number = models.PositiveIntegerField()
#     logins = models.PositiveIntegerField()
#     resources_accessed = models.PositiveIntegerField()
#     total_clicks = models.PositiveIntegerField()

# # Modules Model
# class Module(models.Model):
#     module_id = models.AutoField(primary_key=True)
#     module_name = models.CharField(max_length=100)
#     total_tasks = models.PositiveIntegerField()

#     def __str__(self):
#         return self.module_name

# # Tasks Model
# class Task(models.Model):
#     task_id = models.AutoField(primary_key=True)
#     task_name = models.CharField(max_length=100)
#     module = models.ForeignKey(Module, on_delete=models.CASCADE)
#     deadline = models.DateField()
#     expected_time = models.PositiveIntegerField()  # in minutes
#     type = models.CharField(max_length=50, choices=[('Quiz', 'Quiz'), ('Assignment', 'Assignment'), ('Project', 'Project')])

#     def __str__(self):
#         return self.task_name

# # Task Submissions Model
# class TaskSubmission(models.Model):
#     submission_id = models.AutoField(primary_key=True)
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
#     submission_date = models.DateField()
#     time_taken = models.PositiveIntegerField()  # in minutes
#     score = models.PositiveIntegerField()

# # Industry Training Model
# class IndustryTraining(models.Model):
#     training_id = models.AutoField(primary_key=True)
#     trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
#     hours_completed = models.PositiveIntegerField()
#     feedback_score = models.PositiveIntegerField()
#     milestone = models.CharField(max_length=100)

# # Final Grade Model
# class FinalGrade(models.Model):
#     grade_id = models.AutoField(primary_key=True)
#     trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
#     final_score = models.PositiveIntegerField()
#     certification_status = models.CharField(max_length=10, choices=[('Pass', 'Pass'), ('Fail', 'Fail')])
#  