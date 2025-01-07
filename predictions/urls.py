from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_grade, name='predict_grade'),
]
