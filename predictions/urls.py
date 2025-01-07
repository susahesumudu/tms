from django.urls import path
from . import views

app_name = 'predictions'  # Define the namespace for the app

urlpatterns = [
    path('predict/', views.PredictGradeView.as_view(), name='predict_grade'),
    path('predictions/', views.PredictionListView.as_view(), name='prediction_list'),
        path('predict-row/<int:pk>/', views.PredictForRowView.as_view(), name='predict_for_row'),
path('predictions/<slug:slug>/', views.PredictionDetailView.as_view(), name='prediction_detail'),
]
