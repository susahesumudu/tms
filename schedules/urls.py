from django.urls import path
from .views import CoursePlanView, UpdateCoursePlanView,TrainingPlanView, WeeklyPlanView, LessonPlanView,CoursePlanViewss
from .views import generate_gantt_chart

from .views import generate_gantt_chart_pdf

app_name = 'schedule'


urlpatterns = [
    path ('batch/course/plan', CoursePlanView.as_view(), name='course_plan'),
    path('update-course-plan/', UpdateCoursePlanView.as_view(), name='update_course_plan'),
    #path('batch/<int:batch_id>/course_plan/<int:course_plan_id>/', CoursePlanViews.as_view(), name='course_plans'),
    path("batch/<int:batch_id>/training_plan/<int:training_plan_id>/", TrainingPlanView.as_view(), name="training_plan"),  # Added training_plan_id
    path("batch/<int:batch_id>/weekly_plan/<int:weekly_plan_id>/", WeeklyPlanView.as_view(), name="weekly_plan"),  # Added weekly_plan_id
    path("session/<int:session_id>/lesson_plan/<int:lesson_plan_id>/", LessonPlanView.as_view(), name="lesson_plan"),  # Added lesson_plan_id
    path('batch/<int:course_plan_id>/gantt-chart/', generate_gantt_chart, name='gantt_chart'),
    path('batch/<int:course_plan_id>/gantt-chart-pdf/', generate_gantt_chart_pdf, name='gantt_chart_pdf'),

]
