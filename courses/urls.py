from django.urls import path

from .utils import generate_urlpatterns

app_name = 'courses'

urlpatterns = generate_urlpatterns('courses')