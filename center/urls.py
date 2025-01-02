from django.urls import path

from .utils import generate_urlpatterns

app_name = 'center'

urlpatterns = generate_urlpatterns('center')