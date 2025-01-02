from django.apps import apps
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = "Automatically generate class-based views, URLs, forms, and utilities for Django models."

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str, help="The name of the Django app to generate CRUD.")

    def handle(self, *args, **options):
        app_name = options["app_name"]
        try:
            app_config = apps.get_app_config(app_name)
        except LookupError:
            self.stderr.write(self.style.ERROR(f"App '{app_name}' not found."))
            return

        # Paths
        app_dir = app_config.path
        templates_dir = os.path.join(app_dir, "templates", app_name)
        os.makedirs(templates_dir, exist_ok=True)

        # Content for views.py
        views_content = [
            "from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView",
            "from django.urls import reverse_lazy",
            "from django.apps import apps",
            """
# Base CRUD view classes
class BaseListView(ListView):
    context_object_name = 'items'

    def get_queryset(self):
        model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
        return model.objects.all()

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_list.html"]


class BaseDetailView(DetailView):
    context_object_name = 'item'

    def get_object(self):
        model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
        return model.objects.get(pk=self.kwargs['pk'])

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_detail.html"]


class BaseCreateView(CreateView):
    fields = '__all__'

    def get_queryset(self):
        model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
        return model.objects.all()

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_form.html"]

    def get_success_url(self):
        return reverse_lazy(f"{self.kwargs['model'].lower()}_list")


class BaseUpdateView(UpdateView):
    fields = '__all__'

    def get_object(self):
        model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
        return model.objects.get(pk=self.kwargs['pk'])

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_form.html"]

    def get_success_url(self):
        return reverse_lazy(f"{self.kwargs['model'].lower()}_list")


class BaseDeleteView(DeleteView):

    def get_object(self):
        model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
        return model.objects.get(pk=self.kwargs['pk'])

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_confirm_delete.html"]

    def get_success_url(self):
        return reverse_lazy(f"{self.kwargs['model'].lower()}_list")
            """,
        ]

        # Content for utils.py
        utils_content = [
            "from django.apps import apps",
            "from django.urls import path",
            "from . import views",
            """
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
    return urlpatterns
            """,
        ]

        # Content for urls.py
        urls_content = [
            "from django.urls import path",
            "from .utils import generate_urlpatterns",
            f"app_name = '{app_name}'",
            f"urlpatterns = generate_urlpatterns('{app_name}')",
        ]

        # Content for forms.py
        forms_content = [
            "from django import forms",
            "from django.apps import apps",
            """
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
            """,
        ]

        # File creation
        self.write_file(os.path.join(app_dir, "views.py"), "\n\n".join(views_content))
        self.write_file(os.path.join(app_dir, "utils.py"), "\n\n".join(utils_content))
        self.write_file(os.path.join(app_dir, "urls.py"), "\n\n".join(urls_content))
        self.write_file(os.path.join(app_dir, "forms.py"), "\n\n".join(forms_content))

        # Generate templates
        for model in app_config.get_models():
            model_name = model.__name__.lower()
            for template_name, content in [
                (f"{model_name}_list.html", f"<h1>{model_name.capitalize()} List</h1>\n<ul>\n{{% for item in items %}}\n<li><a href=\"{{{{ item.get_absolute_url }}}}\">{{{{ item }}}}</a></li>\n{{% endfor %}}\n</ul>"),
                (f"{model_name}_detail.html", f"<h1>{model_name.capitalize()} Detail</h1>\n<p>{{{{ item }}}}</p>\n<a href=\"{{% url '{model_name}_update' item.id %}}\">Edit</a>\n<a href=\"{{% url '{model_name}_delete' item.id %}}\">Delete</a>"),
                (f"{model_name}_form.html", f"<h1>{model_name.capitalize()} Form</h1>\n<form method=\"post\">\n  {{% csrf_token %}}\n  {{{{ form.as_p }}}}\n  <button type=\"submit\">Save</button>\n</form>"),
                (f"{model_name}_confirm_delete.html", f"<h1>Confirm Delete {model_name.capitalize()}</h1>\n<p>Are you sure you want to delete {{{{ item }}}}? </p>\n<form method=\"post\">\n  {{% csrf_token %}}\n  <button type=\"submit\">Yes</button>\n</form>\n<a href=\"{{% url '{model_name}_list' %}}\">Cancel</a>"),
            ]:
                self.write_template(os.path.join(templates_dir, template_name), content)

        self.stdout.write(self.style.SUCCESS(f"CRUD for app '{app_name}' generated successfully!"))

    def write_file(self, path, content):
        with open(path, "w") as file:
            file.write(content)

    def write_template(self, path, content):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as template_file:
            template_file.write(content)
