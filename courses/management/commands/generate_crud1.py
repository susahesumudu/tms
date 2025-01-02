import os
from django.apps import apps
from django.core.management.base import BaseCommand


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

        # Generate base templates and model-specific templates
        self.generate_base_templates(app_name)
        self.generate_model_templates(app_name, app_config.get_models())

        self.stdout.write(self.style.SUCCESS(f"CRUD templates for app '{app_name}' generated successfully!"))

    def generate_base_templates(self, app_name):
        """
        Creates base templates for list, detail, form, and confirm delete pages.
        These are used for template inheritance by the model-specific templates.
        """
        base_template_dir = os.path.join(app_name, 'templates', app_name)
        os.makedirs(base_template_dir, exist_ok=True)

        # base_list.html
        base_list_path = os.path.join(base_template_dir, 'base_list.html')
        if not os.path.exists(base_list_path):
            with open(base_list_path, 'w') as f:
                f.write("""{% extends "base.html" %}
{% block title %}{{ model|capfirst }} List{% endblock %}

{% block content %}
<h1>{{ model|capfirst }} List</h1>
<table>
  <thead>
    <tr>
      {% for field in fields %}
      <th>{{ field }}</th>
      {% endfor %}
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    {% for item in items %}
    <tr>
      {% for field in fields %}
      <td>{{ item|getattr:field }}</td>
      {% endfor %}
      <td>
        <a href="{{ item|get_url:'detail' }}">View</a>
        <a href="{{ item|get_url:'update' }}">Edit</a>
        <a href="{{ item|get_url:'delete' }}">Delete</a>
      </td>
    </tr>
    {% empty %}
    <tr><td colspan="{{ fields|length + 1 }}">No {{ model|lower }} found.</td></tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
""")

        # base_confirm_delete.html
        base_delete_path = os.path.join(base_template_dir, 'base_confirm_delete.html')
        if not os.path.exists(base_delete_path):
            with open(base_delete_path, 'w') as f:
                f.write("""{% extends "base.html" %}
{% block title %}Delete {{ model|capfirst }}{% endblock %}

{% block content %}
<h1>Are you sure you want to delete this {{ model|lower }}?</h1>
<form method="POST">
  {% csrf_token %}
  <button type="submit">Confirm Delete</button>
</form>
{% endblock %}
""")

    def generate_model_templates(self, app_name, models):
        """
        Generate the model-specific templates that extend the base templates.
        """
        base_template_dir = os.path.join(app_name, 'templates', app_name)
        os.makedirs(base_template_dir, exist_ok=True)

        for model in models:
            model_name = model.__name__.lower()
            fields = [field.name for field in model._meta.fields]

            self.generate_list_template(base_template_dir, model_name, app_name, fields)
            self.generate_detail_template(base_template_dir, model_name, app_name, fields)
            self.generate_form_template(base_template_dir, model_name, app_name)
            self.generate_confirm_delete_template(base_template_dir, model_name, app_name)

    def generate_list_template(self, base_template_dir, model_name, app_name, fields):
          template_file_path = os.path.join(base_template_dir, f"{model_name}_list.html")
          if not os.path.exists(template_file_path):
              with open(template_file_path, 'w') as f:
                  f.write("{% extends 'base_list.html' %}\n")
                  f.write("{% block content %}\n")
                  f.write("<h1>{{ model|capfirst }} List</h1>\n")
                  f.write("<table class='table'>\n")
                  f.write("  <thead>\n    <tr>\n")
                  for field in fields:
                      f.write(f"      <th>{field}</th>\n")
                  f.write("      <th>Actions</th>\n    </tr>\n  </thead>\n")
                  f.write("  <tbody>\n")
                  f.write("    {% for item in items %}\n    <tr>\n")
                  for field in fields:
                      f.write(f"      <td>{{{{ item.{field} }}}}</td>\n")
                  f.write("      <td>\n")
                  f.write("        <a href=\"{% url '" + app_name + ":" + model_name + "_detail' pk=item.pk %}\">View</a>\n")
                  f.write("        <a href=\"{% url '" + app_name + ":" + model_name + "_update' pk=item.pk %}\">Edit</a>\n")
                  f.write("        <a href=\"{% url '" + app_name + ":" + model_name + "_delete' pk=item.pk %}\">Delete</a>\n")
                  f.write("      </td>\n    </tr>\n    {% empty %}\n")
                  f.write("    <tr><td colspan='{{ column_count }}'>No {{ model|lower }} found.</td></tr>\n")
                  f.write("    {% endfor %}\n  </tbody>\n</table>\n")
                  f.write("{% endblock %}\n")



    def generate_detail_template(self, base_template_dir, model_name, app_name, fields):
        template_file_path = os.path.join(base_template_dir, f"{model_name}_detail.html")
        if not os.path.exists(template_file_path):
            with open(template_file_path, 'w') as f:
                f.write("{% extends 'base_detail.html' %}\n")
                f.write("{% block content %}\n")
                f.write(f"<h1>{{{{ model|capfirst }}}} Detail</h1>\n")
                for field in fields:
                    f.write(f"<p>{field.capitalize()}: {{{{ item.{field} }}}}</p>\n")
                f.write("{% endblock %}\n")

    def generate_form_template(self, base_template_dir, model_name, app_name):
        template_file_path = os.path.join(base_template_dir, f"{model_name}_form.html")
        if not os.path.exists(template_file_path):
            with open(template_file_path, 'w') as f:
                f.write("{% extends 'base_form.html' %}\n")
                f.write("{% block content %}\n")
                f.write(f"<h1>Create / Update {{{{ model|capfirst }}}}</h1>\n")
                f.write("<form method='POST'>\n")
                f.write("  {% csrf_token %}\n")
                f.write("  {{{{ form.as_p }}}}\n")
                f.write("  <button type='submit'>Save</button>\n")
                f.write("</form>\n")
                f.write("{% endblock %}\n")

    def generate_confirm_delete_template(self, base_template_dir, model_name, app_name):
        template_file_path = os.path.join(base_template_dir, f"{model_name}_confirm_delete.html")
        if not os.path.exists(template_file_path):
            with open(template_file_path, 'w') as f:
                f.write("{% extends 'base_confirm_delete.html' %}\n")
                f.write("{% block content %}\n")
                f.write(f"<h1>Are you sure you want to delete this {{{{ model|lower }}}}</h1>\n")
                f.write("<form method='POST'>\n")
                f.write("  {% csrf_token %}\n")
                f.write("  <button type='submit'>Confirm Delete</button>\n")
                f.write("</form>\n")
                f.write("{% endblock %}\n")
