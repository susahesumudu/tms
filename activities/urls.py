from django.urls import path

from .utils import generate_urlpatterns

app_name = 'activities'

urlpatterns = generate_urlpatterns('activities')