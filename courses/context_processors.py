# courses/context_processors.py

from django.apps import apps

def courses_models(request):
    """
    Adds a list of models from the 'courses' app to the template context.
    Each model is represented as a dictionary with:
    - 'name': The lowercase name of the model.
    - 'verbose_name_plural': The plural verbose name of the model.
    - 'url_name': The namespaced URL name for the model's list view.
    - 'url_short_name': The short URL name for active link detection.
    - 'create_url_name': The namespaced URL name for the model's create view.
    """
    app_name = 'courses'  # Replace with your app name if different
    try:
        app_config = apps.get_app_config(app_name)
    except LookupError:
        return {'courses_models': []}  # App not found; return empty list

    models = app_config.get_models()
    model_info = []
    for model in models:
        model_lower = model.__name__.lower()
        model_info.append({
            'name': model_lower,
            'verbose_name_plural': model._meta.verbose_name_plural,
            'url_name': f'courses:{model_lower}_list',          # e.g., 'exercises:skill_list'
            'url_short_name': f'{model_lower}_list',            # e.g., 'skill_list'
            'create_url_name': f'courses:{model_lower}_create',# e.g., 'exercises:skill_create'
        })
    return {'courses_models': model_info}
