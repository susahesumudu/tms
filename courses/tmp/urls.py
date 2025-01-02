from django.urls import path
from .views import (
    CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView, CourseDeleteView,
    ModuleListView, ModuleDetailView, ModuleCreateView, ModuleUpdateView, ModuleDeleteView,
    TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    SessionListView, SessionDetailView, SessionCreateView, SessionUpdateView, SessionDeleteView,
    ActivityListView, ActivityDetailView, ActivityCreateView, ActivityUpdateView, ActivityDeleteView,
)

# Common structure for URLs
def generate_crud_urls(base_name, list_view, detail_view, create_view, update_view, delete_view):
    return [
        path(f'{base_name}s/', list_view.as_view(), name=f'{base_name}_list'),
        path(f'{base_name}s/<int:pk>/', detail_view.as_view(), name=f'{base_name}_detail'),
        path(f'{base_name}s/create/', create_view.as_view(), name=f'{base_name}_create'),
        path(f'{base_name}s/<int:pk>/update/', update_view.as_view(), name=f'{base_name}_update'),
        path(f'{base_name}s/<int:pk>/delete/', delete_view.as_view(), name=f'{base_name}_delete'),
    ]

# URL patterns
urlpatterns = []

# Append URLs for each model
urlpatterns += generate_crud_urls(
    'course',
    CourseListView, CourseDetailView, CourseCreateView, CourseUpdateView, CourseDeleteView
)
urlpatterns += generate_crud_urls(
    'module',
    ModuleListView, ModuleDetailView, ModuleCreateView, ModuleUpdateView, ModuleDeleteView
)
urlpatterns += generate_crud_urls(
    'task',
    TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView
)
urlpatterns += generate_crud_urls(
    'session',
    SessionListView, SessionDetailView, SessionCreateView, SessionUpdateView, SessionDeleteView
)
urlpatterns += generate_crud_urls(
    'activity',
    ActivityListView, ActivityDetailView, ActivityCreateView, ActivityUpdateView, ActivityDeleteView
)
