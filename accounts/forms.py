from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile, TeacherProfile, StaffProfile, ParentProfile
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label="Username",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password",
    )


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label="Email",
    )

    class Meta:
        model = User
        fields = ['username', 'email']  # Removed 'password1' and 'password2'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data


class ProfileFormMixin(forms.ModelForm):
    """Base form mixin for common fields."""
    class Meta:
        fields = '__all__'
        exclude = ['user']


class StudentProfileForm(ProfileFormMixin):
    class Meta(ProfileFormMixin.Meta):
        model = StudentProfile
        fields = '__all__'  # Includes the avatar field


class TeacherProfileForm(ProfileFormMixin):
    class Meta(ProfileFormMixin.Meta):
        model = TeacherProfile
        fields = '__all__'  # Includes the avatar field


class StaffProfileForm(ProfileFormMixin):
    class Meta(ProfileFormMixin.Meta):
        model = StaffProfile
        fields = '__all__'  # Includes the avatar field


class ParentProfileForm(ProfileFormMixin):
    class Meta(ProfileFormMixin.Meta):
        model = ParentProfile
        fields = '__all__'  # Includes the avatar field