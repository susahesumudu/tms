from django.apps import apps

from django.urls import path

from . import views


def generate_urlpatterns(app_name):
    urlpatterns = []
    app_config = apps.get_app_config(app_name)
    for model in app_config.get_models():
        model_name = model.__name__.lower()
        urlpatterns += [
            path(f'{model_name}/', views.BaseListView.as_view(), name=f'{model_name}_list', kwargs={'app_name': app_name, 'model': model_name}),
            path(f'{model_name}/<int:pk>/', views.BaseDetailView.as_view(), name=f'{model_name}_detail', kwargs={'app_name': app_name, 'model': model_name}),
            path(f'{model_name}/new/', views.BaseCreateView.as_view(), name=f'{model_name}_create', kwargs={'app_name': app_name, 'model': model_name}),
            path(f'{model_name}/<int:pk>/edit/', views.BaseUpdateView.as_view(), name=f'{model_name}_update', kwargs={'app_name': app_name, 'model': model_name}),
            path(f'{model_name}/<int:pk>/delete/', views.BaseDeleteView.as_view(), name=f'{model_name}_delete', kwargs={'app_name': app_name, 'model': model_name}),
        ]

    urlpatterns += [
        path(
            'exercise/questions/<int:pk>',
            views.ExerciseDetailView.as_view(),
            name='exercise_custom_detail'
        ),
    ]
    return urlpatterns
            