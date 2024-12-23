
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import render


from django.http import Http404


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from .models import Profile
from .forms import ProfileForm


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class CreateProfileView(View):
    def post(self, request):
        # Check if the user already has a profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        if not created:
            # If the profile already exists, redirect to the profile detail view
            return redirect('profile_detail')
        return redirect('profile_detail')  # Redirect after creating the profile






class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'





class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')




class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'

    def get_object(self, queryset=None):
        try:
            # Attempt to fetch the profile associated with the user
            return self.request.user.profile
        except Profile.DoesNotExist:
            # Redirect to create_profile if the profile does not exist
            return redirect('create_profile')


# Profile Update View
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('profile-detail')

    def get_object(self):
        # Ensure the logged-in user edits their profile
        return self.request.user.profile




   