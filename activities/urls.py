from django.urls import path

from .utils import generate_urlpatterns
from . import views

app_name = 'activities'

urlpatterns = generate_urlpatterns('activities')
urlpatterns += [
    
            path(
                'exercise/questions/<int:pk>',
                views.ExerciseDetailViews.as_view(),  # Make sure it's ExerciseDetailView
                name='exercise_custom_detail'
            ),
            path(
                'exercise/questions/submit/<int:exercise_id>',
                views.SubmitExerciseView.as_view(),
                name='exercise_submit_exercise'
            ),
            path(
                'exercise/questions/mark-completed',
             views.MarkQuestionCompletedView.as_view(), name='mark_question_completed'),            
            
            path(
                'activity/<slug:slug>/exercises',
             views.ActivityExerciseListView.as_view(), name='activity_exercises_list'),            
            
             path(
                'exercises/<slug:slug>/questions',
             views.ActivityExerciseDetailView.as_view(), name='exercise_detail_quesions'),            
            
            
             path(
                'exercises/<slug:slug>/questions/new',
             views.ActivityExerciseAddQuestion.as_view(), name='exercise_new_quesions'),   

            path(     
                'exercises/<slug:slug>/grade',
             views.GradeExerciseView.as_view(), name='grade_exercise'),      

                        path(     
                'exercises/<slug:slug>/submit',
             views.SubmitExerciseView.as_view(), name='submit_exercise'),          
            
            ]


            