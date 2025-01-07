from django import forms
from django.contrib.auth.models import User, Group
from activities.models import QuizSubmission, Submission, Quiz, Exercise

# Helper function to get users in the "Student" group
def get_students():
    try:
        student_group = Group.objects.get(name="Student")  # Assumes the group is named "Student"
        return User.objects.filter(groups=student_group)
    except Group.DoesNotExist:
        return User.objects.none()  # Return an empty queryset if the group doesn't exist

class AssignExerciseForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=get_students(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Student"
    )
    exercise = forms.ModelChoiceField(
        queryset=Exercise.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Exercise"
    )

    class Meta:
        model = Submission
        fields = ['student', 'exercise']

class AssignQuizForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=get_students(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Student"
    )
    quiz = forms.ModelChoiceField(
        queryset=Quiz.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Quiz"
    )

    class Meta:
        model = QuizSubmission
        fields = ['user', 'quiz']
