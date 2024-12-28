from django import forms
from .models import Course,Module

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'  # Specify fields explicitly if needed


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = '__all__'  # Specify fields explicitly if needed


class TaskForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = '__all__'  # Specify fields explicitly if needed

class SessionForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = '__all__'  # Specify fields explicitly if needed

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = '__all__'  # Specify fields explicitly if needed
