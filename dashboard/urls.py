
from django.urls import path
from .views import DashboardRedirectView, AdminDashboardView, TeacherDashboardView, StudentDashboardView

urlpatterns = [
    path('', DashboardRedirectView.as_view(), name='dashboard_redirect'),
    path('admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('teacher/', TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('student/', StudentDashboardView.as_view(), name='student_dashboard'),
]