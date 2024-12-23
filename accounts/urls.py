
from django.urls import path
from .views import LoginView, LogoutView, DashboardView
from .views import ProfileDetailView, ProfileUpdateView,CreateProfileView,SignupView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),  # Verify this line exists
    path('profile/create/', CreateProfileView.as_view(), name='create_profile'),
    path('signup/', SignupView.as_view(), name='signup'),

]
        

