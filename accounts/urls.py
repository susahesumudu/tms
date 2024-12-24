from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    SignupView,
    ProfileUpdateView,
    ProfileDetailView,
)

urlpatterns = [
    # Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),

    # Profile Management
    path('profile/edit/<str:profile_type>/', ProfileUpdateView.as_view(), name='profile_edit'),
        path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
]


