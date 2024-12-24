from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import FormView, UpdateView, View
from django.urls import reverse_lazy
from .forms import LoginForm, SignupForm, StudentProfileForm, TeacherProfileForm, StaffProfileForm, ParentProfileForm
from .models import StudentProfile, TeacherProfile, StaffProfile, ParentProfile
from django.views.generic import DetailView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import Http404


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


class LogoutView(LoginRequiredMixin, View):
    """Logs out the user and redirects to the login page."""
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class SignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  # Hash the password
        user.save()
        return super().form_valid(form)




class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/profile_update.html'
    success_url = '/accounts/profile/'  # Redirect to profile detail after editing
    form_class = None

    def get_object(self):
        """Fetch the profile object based on the user and profile type."""
        user = self.request.user
        profile_type = self.kwargs.get('profile_type')

        # Map profile types to their respective models
        profile_mapping = {
            'teacher': TeacherProfile,
            'student': StudentProfile,
            'staff': StaffProfile,
            'parent': ParentProfile,
        }

        if profile_type not in profile_mapping:
            raise ValueError(f"Invalid profile type: {profile_type}")

        # Fetch the correct profile object
        return get_object_or_404(profile_mapping[profile_type], user=user)

    def get_form_class(self):
        """Return the appropriate form based on the profile type."""
        profile_type = self.kwargs.get('profile_type')

        # Map profile types to their respective forms
        form_mapping = {
            'teacher': TeacherProfileForm,
            'student': StudentProfileForm,
            'staff': StaffProfileForm,
            'parent': ParentProfileForm,
        }

        if profile_type not in form_mapping:
            raise ValueError(f"Invalid profile type: {profile_type}")

        return form_mapping[profile_type]

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())






class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        user = self.request.user

        # Determine the profile type and get the profile object
        if user.groups.filter(name='Teacher').exists():
            self.profile_type = 'teacher'
            return get_object_or_404(TeacherProfile, user=user)
        elif user.groups.filter(name='Student').exists():
            self.profile_type = 'student'
            return get_object_or_404(StudentProfile, user=user)
        elif user.groups.filter(name='Staff').exists():
            self.profile_type = 'staff'
            return get_object_or_404(StaffProfile, user=user)
        elif user.groups.filter(name='Parent').exists():
            self.profile_type = 'parent'
            return get_object_or_404(ParentProfile, user=user)
        raise Http404("Profile not found.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add profile type to context
        context['profile_type'] = getattr(self, 'profile_type', None)

        # Add profile_edit_url to context if profile_type exists
        if context['profile_type']:
            context['profile_edit_url'] = reverse('profile_edit', kwargs={'profile_type': context['profile_type']})
        else:
            context['profile_edit_url'] = None

        return context



