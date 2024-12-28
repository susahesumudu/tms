from django.urls import path
from .views import CoursePlanView, TrainingPlanView, WeeklyPlanView, LessonPlanView
from .views import generate_gantt_chart

from .views import generate_gantt_chart_pdf



urlpatterns = [
    path('batch/<int:batch_id>/course_plan/<int:course_plan_id>/', CoursePlanView.as_view(), name='course_plan'),
    path("batch/<int:batch_id>/training_plan/<int:training_plan_id>/", TrainingPlanView.as_view(), name="training_plan"),  # Added training_plan_id
    path("batch/<int:batch_id>/weekly_plan/<int:weekly_plan_id>/", WeeklyPlanView.as_view(), name="weekly_plan"),  # Added weekly_plan_id
    path("session/<int:session_id>/lesson_plan/<int:lesson_plan_id>/", LessonPlanView.as_view(), name="lesson_plan"),  # Added lesson_plan_id
    path('batch/<int:course_plan_id>/gantt-chart/', generate_gantt_chart, name='gantt_chart'),
    path('batch/<int:course_plan_id>/gantt-chart-pdf/', generate_gantt_chart_pdf, name='gantt_chart_pdf'),

]

