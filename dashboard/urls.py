
from django.urls import path
from .views import DashboardRedirectView, TeacherDashboardView, StudentDashboardView

urlpatterns = [
    path('', DashboardRedirectView.as_view(), name='dashboard'),
       path('redirect/', DashboardRedirectView.as_view(), name='dashboard_redirect'),
    path('teacher/', TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('student/', StudentDashboardView.as_view(), name='student_dashboard'),
]

