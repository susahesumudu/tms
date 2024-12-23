from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

class DashboardRedirectView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user.groups.filter(name='Admin').exists():
            return redirect('admin_dashboard')
        elif user.groups.filter(name='Teacher').exists():
            return redirect('teacher_dashboard')
        elif user.groups.filter(name='Student').exists():
            return redirect('student_dashboard')

        return HttpResponseForbidden("You don't have access to any dashboard.")

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/admin_dashboard.html'

class TeacherDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/teacher_dashboard.html'

class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/student_dashboard.html'
