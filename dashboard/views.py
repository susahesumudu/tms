from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from accounts.models import StudentProfile,TeacherProfile
from courses.models import Activity
from activities.models import *
from accounts.models import StudentProfile

from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardRedirectView(LoginRequiredMixin, TemplateView):
    """Redirect users to their role-specific dashboard."""
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Teacher').exists():
            return redirect('teacher_dashboard')
        elif user.groups.filter(name='Student').exists():
            return redirect('student_dashboard')
        elif user.groups.filter(name='Admin').exists() or user.is_superuser:
            return redirect('/admin/')
        return redirect('default_dashboard')  # Fallback


 

class TeacherDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/teacher_dashboard.html'
    login_url = 'login'  # Redirect to login if not authenticated


class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/student_dashboard.html'
    login_url = 'login'  # Redirect to login if not authenticated
    # def get_context_data(self, **kwargs):
    #         context = super().get_context_data(**kwargs)
    #         activities = Activity.objects.filter(student=self.request.user)
    #         marks_tracker, created = MarksTracker.objects.get_or_create(student=self.request.user)

    #         context['activities'] = activities
    #         context['marks_tracker'] = marks_tracker
    #         return context  


class StaffDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/staff_dashboard.html'


class ParentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/parent_dashboard.html'
  

