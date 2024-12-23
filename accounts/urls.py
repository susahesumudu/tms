
from django.urls import path
from .views import LoginView, LogoutView, DashboardView
from .views import ProfileDetailView, ProfileUpdateView,CreateProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
     path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
        path('create-profile/', CreateProfileView.as_view(), name='create_profile'),
]
        

