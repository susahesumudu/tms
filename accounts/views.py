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


import json
import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import ClickLog, Activity, Exercise

logger = logging.getLogger(__name__)

def get_client_ip(request):
    """
    Utility to extract the client's IP address.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()  # Take the first IP in the chain
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_ip(request):
    """
    Utility to extract the client's IP address.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def capture_click(request):
    """
    Handles click capture events, logging click details to the database.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method. Only POST is allowed."}, status=405)

    if request.content_type != "application/json":
        return JsonResponse({"error": "Invalid content type. Expected 'application/json'"}, status=400)

    try:
        # Parse JSON payload
        data = json.loads(request.body)
        logger.info(f"Click data received: {data}")

        # Extract data from JSON
        url = data.get('url')
        element_id = data.get('element_id')
        element_tag = data.get('element_tag')
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Validate required fields
        if not url or not element_tag:
            return JsonResponse(
                {"error": "Missing required fields: 'url' and 'element_tag' are mandatory."},
                status=400
            )

        # Extract slugs for activity and exercise
        slugs = extract_slug(url)
        activity_slug = slugs.get('activity_slug')
        exercise_slug = slugs.get('exercise_slug')

        activity = None
        exercise = None

        if activity_slug:
            activity = get_object_or_404(Activity, slug=activity_slug)

        if exercise_slug:
            exercise = get_object_or_404(Exercise, slug=exercise_slug)

        # Save ClickLog
        ClickLog.objects.create(
            url=url,
            element_id=element_id,
            element_tag=element_tag,
            user=request.user if request.user.is_authenticated else None,
            activity=activity,
            exercise=exercise,
            ip_address=ip_address,
            user_agent=user_agent
        )

        logger.info("Click successfully logged.")
        return JsonResponse({"message": "Click recorded successfully"}, status=201)

    except json.JSONDecodeError:
        logger.error("Invalid JSON payload")
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({"error": f"Unexpected error occurred: {str(e)}"}, status=500)

def extract_slug(url):
    """
    Extract the slug from the URL for both exercise and activity.

    Args:
        url (str): The URL string to parse.

    Returns:
        dict: A dictionary containing the slugs for 'exercise' and 'activity', if found.
    """
    import re

    # Patterns for exercise and activity slugs
    exercise_pattern = r"exercises/([\w-]+)"
    activity_pattern = r"activity/([\w-]+)"

    # Initialize result
    result = {'activity_slug': None, 'exercise_slug': None}

    # Match for activity slug
    activity_match = re.search(activity_pattern, url)
    if activity_match:
        result['activity_slug'] = activity_match.group(1)

    # Match for exercise slug
    exercise_match = re.search(exercise_pattern, url)
    if exercise_match:
        result['exercise_slug'] = exercise_match.group(1)

    return result