from django import forms

from django.apps import apps


from django import forms
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured

def generate_dynamic_form(app_name, model_name, fields=None, widgets=None):
    """
    Generate a dynamic ModelForm for a given model in the specified app.
    
    :param app_name: The name of the Django app.
    :param model_name: The name of the model.
    :param fields: Optional list of fields to include. Defaults to all fields.
    :param widgets: Optional dictionary of widgets for customizing field rendering.
    :return: A dynamically created ModelForm class.
    """
    try:
        model = apps.get_model(app_label=app_name, model_name=model_name)
    except LookupError:
        raise ImproperlyConfigured(f"Model '{model_name}' not found in app '{app_name}'.")

    class Meta:
        model = model
        fields = fields if fields else '__all__'
        if widgets:
            form_widgets = widgets
        else:
            form_widgets = {}

    # Return the dynamically created form class
    return type(
        f'{model_name}Form',
        (forms.ModelForm,),
        {'Meta': Meta, 'form_widgets': form_widgets}
    )


def create_dynamic_forms(app_name, fields=None, widgets=None):
    """
    Generate dynamic forms for all models in a specified Django app.
    
    :param app_name: The name of the Django app.
    :param fields: Optional list of fields to include for all forms.
    :param widgets: Optional dictionary of widgets for customizing field rendering.
    :return: A dictionary of dynamic forms where keys are model names and values are form classes.
    """
    try:
        app_config = apps.get_app_config(app_name)
    except LookupError:
        raise ImproperlyConfigured(f"App '{app_name}' not found.")

    forms_dict = {}
    for model in app_config.get_models():
        model_name = model.__name__
        forms_dict[model_name] = generate_dynamic_form(app_name, model_name, fields, widgets)

    return forms_dict
