from django.db import models
from django.core.exceptions import ValidationError

class Course(models.Model):
   
    
    DELIVERY_MODE_CHOICES = [
        ('classroom', 'Classroom'),
        ('online', 'Online'),
        ('blended', 'Blended (both classroom & online)'),
    ]
    
    COURSE_MODE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
    ]

    COURSE_MEDIAUM_CHOICES = [
        ('sinhala_lng','SINHALA'),
        ('english_lng','ENGLISH'),

    ]
    
    # Fields
    course_name = models.CharField(max_length=200, unique=True)  # Course Title
    course_code = models.CharField(max_length=50, unique=True)  # Course Code
    entry_qualification = models.CharField(max_length=200)  # Entry Qualification
    medium = models.CharField(max_length=100 ,choices=COURSE_MEDIAUM_CHOICES)  # Medium
    course_duration_months =models.PositiveIntegerField()  # Course Duration in months
    delivery_mode = models.CharField(max_length=50, choices=DELIVERY_MODE_CHOICES)  # Delivery Mode
    course_mode = models.CharField(max_length=50, choices=COURSE_MODE_CHOICES)  # Course Mode
    curriculum_availability = models.BooleanField(default=True) # Curriculum Availability
    no_of_batches_per_year = models.PositiveIntegerField()  # Number of Batches per Year
    max_students_per_batch = models.PositiveIntegerField()  # Max Students per Batch
    course_fee = models.DecimalField(max_digits=10, decimal_places=2)  # Course Fee
    course_cost = models.DecimalField(max_digits=10, decimal_places=2)  # Course Fee
    is_active = models.BooleanField(default=True)  # Active status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    theory_hrs = models.PositiveIntegerField() 
    practical_hrs = models.PositiveIntegerField() 

    def __str__(self):
        return self.course_name

    


      







class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    module_name = models.CharField(max_length=200)
    moduel_code = models.CharField(max_length=200)
    theory_hours = models.PositiveIntegerField()
    practical_hours = models.PositiveIntegerField()
    module_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    module_duration_weeks =models.PositiveIntegerField()  # Course Duration in months
    def __str__(self):
        return self.module_name
   
        
   


class Task(models.Model):
    module = models.ForeignKey(Module, related_name='tasks', on_delete=models.CASCADE)
    task_name = models.CharField(max_length=200)
    task_code = models.CharField(max_length=10)
    theory_hours = models.PositiveIntegerField()
    practical_hours = models.PositiveIntegerField()
    task_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the instance is created
    updated_at = models.DateTimeField(auto_now=True)      # Automatically updated when the instance is saved
    task_duration_days =models.PositiveIntegerField()  # Course Duration in months
    def __str__(self):
        return self.task_name