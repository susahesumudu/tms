from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm, LoginForm,SignupForm
from django.contrib.auth.decorators import login_required
from django.views import View


@method_decorator(login_required, name='dispatch')
class CreateProfileView(View):
    def get(self, request):
        return render(request, 'accounts/create_profile.html')

    def post(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        return redirect('create_profile')  # Redirect to the profile detail page





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




@method_decorator(login_required, name='dispatch')
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'

    def get_object(self, queryset=None):
        try:
            # Fetch the user's profile
            return self.request.user.profile
        except Profile.DoesNotExist:
            # Redirect to create profile if not found
            return redirect('create_profile')


# Profile Update View
@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_update.html'
    success_url = '/accounts/profile/'  # Redirect to profile detail after editing

    def get_object(self, queryset=None):
        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            raise Http404("Profile not found")


   



class SignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Create a new user
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  # Hash the password
        user.save()
        return super().form_valid(form)
