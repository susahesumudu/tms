from django import forms

from django.apps import apps


def generate_dynamic_form(app_name, model_name):
    model = apps.get_model(app_label=app_name, model_name=model_name)
    class Meta:
        model = model
        fields = '__all__'
    return type(f'{model_name}Form', (forms.ModelForm,), {'Meta': Meta})


def create_dynamic_forms(app_name):
    app_config = apps.get_app_config(app_name)
    forms = {}
    for model in app_config.get_models():
        model_name = model.__name__.lower()
        forms[model_name] = generate_dynamic_form(app_name, model_name)
    return forms
            