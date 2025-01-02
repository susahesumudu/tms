import os
from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Generates base templates and model-specific CRUD templates for each model in the app'

    def handle(self, *args, **kwargs):
        app_name = 'exercises'  # Replace with your app name
        app_config = apps.get_app_config(app_name)
        models = app_config.get_models()

        # First, generate the "base" templates used for inheritance
        self.generate_base_templates(app_name)

        # Then, generate the model-specific templates (list, detail, form, confirm_delete)
        self.generate_model_templates(app_name, models)

    def generate_base_templates(self, app_name):
        """
        Creates base templates for list, detail, form, and confirm delete pages.
        These are used for template inheritance by the model-specific templates.
        """
        base_template_dir = os.path.join(app_name, 'templates')
        os.makedirs(base_template_dir, exist_ok=True)

        # base_list.html
        base_list_path = os.path.join(base_template_dir, 'base_list.html')
        if not os.path.exists(base_list_path):
            with open(base_list_path, 'w') as f:
                f.write("""{% extends "base.html" %}
{% block title %}{{ model|capfirst }} List{% endblock %}

{% block content %}
<a href="{{% url '{app_name}:{model_name}_create' %}}" class="btn btn-sm btn-success mb-3">Add New</a>
<!-- This is the generic layout for listing items. Child templates can override or extend. -->
<h1>{{ model|capfirst }} List</h1>
<table>
  <thead>
    <tr>
      <th>ID</th>
      <th>Name</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    {% for item in items %}
    <tr>
      <td>{{ item.id }}</td>
      <td>{{ item.name }}</td>
      <td>
        <!-- Example URLs (adjust for your namespacing) -->
        <!-- <a href="{% url 'exercises:model_detail' pk=item.pk %}">View</a> -->
        <!-- <a href="{% url 'exercises:model_update' pk=item.pk %}">Edit</a> -->
        <!-- <a href="{% url 'exercises:model_delete' pk=item.pk %}">Delete</a> -->
      </td>
    </tr>
    {% empty %}
    <tr><td colspan="3">No {{ model|lower }} found.</td></tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
""")

        # base_detail.html
        base_detail_path = os.path.join(base_template_dir, 'base_detail.html')
        if not os.path.exists(base_detail_path):
            with open(base_detail_path, 'w') as f:
                f.write("""{% extends "base.html" %}
{% block title %}{{ model|capfirst }} Detail{% endblock %}

{% block content %}
<!-- This is the generic layout for displaying detail of one item. -->
<h1>{{ model|capfirst }} Detail</h1>
<p>ID: {{ item.id }}</p>
<p>Name: {{ item.name }}</p>
<p>Description: {{ item.description }}</p>
<!-- Add or override fields as needed in child templates. -->
{% endblock %}
""")

        # base_form.html
        base_form_path = os.path.join(base_template_dir, 'base_form.html')
        if not os.path.exists(base_form_path):
            with open(base_form_path, 'w') as f:
                f.write("""{% extends "base.html" %}
{% block title %}{{ model|capfirst }} Form{% endblock %}

{% block content %}
<!-- Generic layout for create/update forms -->
<h1>{{ model|capfirst }} Form</h1>
<form method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Save</button>
</form>
{% endblock %}
""")

        # base_confirm_delete.html
        base_delete_path = os.path.join(base_template_dir, 'base_confirm_delete.html')
        if not os.path.exists(base_delete_path):
            with open(base_delete_path, 'w') as f:
                f.write("""{% extends "base.html" %}
{% block title %}Delete {{ model|capfirst }}{% endblock %}

{% block content %}
<!-- Generic layout for delete confirmation -->
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
            self.generate_list_template(base_template_dir, model_name)
            self.generate_detail_template(base_template_dir, model_name)
            self.generate_form_template(base_template_dir, model_name)
            self.generate_confirm_delete_template(base_template_dir, model_name)

    # ----------------------
    # MODEL-SPECIFIC FILES
    # ----------------------
    def generate_list_template(self, base_template_dir, model_name):
        template_file_path = os.path.join(base_template_dir, f"{model_name}_list.html")
        if not os.path.exists(template_file_path):
            with open(template_file_path, 'w') as f:
                f.write("{% extends 'base_list.html' %}\n")
                f.write("{% block content %}\n")
                f.write(f"<!-- Template for {model_name} list -->\n")
                f.write(f"<h1>{{{{ model|capfirst }}}} List</h1>\n")
                
                # Add New button
                f.write(f"<a href=\"{{% url 'exercises:{model_name}_create' %}}\" class=\"btn btn-sm btn-success mb-3\">Add New</a>\n")
                
                f.write("<table class=\"table\">\n")
                f.write("  <thead>\n    <tr>\n      <th>ID</th>\n      <th>Name</th>\n      <th>Actions</th>\n    </tr>\n  </thead>\n")
                f.write("  <tbody>\n")
                f.write("    {% for item in items %}\n")
                f.write("    <tr>\n      <td>{{ item.id }}</td>\n      <td>{{ item.name }}</td>\n      <td>\n")
                f.write(f"        <a href=\"{{% url 'exercises:{model_name}_detail' pk=item.pk %}}\">View</a> \n")
                f.write(f"        <a href=\"{{% url 'exercises:{model_name}_update' pk=item.pk %}}\">Edit</a> \n")
                f.write(f"        <a href=\"{{% url 'exercises:{model_name}_delete' pk=item.pk %}}\">Delete</a>\n")
                f.write("      </td>\n    </tr>\n")
                f.write("    {% empty %}\n    <tr><td colspan=\"3\">No {{ model|lower }} found.</td></tr>\n")
                f.write("    {% endfor %}\n")
                f.write("  </tbody>\n")
                f.write("</table>\n")
                f.write("<!-- End of list template -->\n")
                f.write("{% endblock %}\n")


    def generate_detail_template(self, base_template_dir, model_name):
        template_file_path = os.path.join(base_template_dir, f"{model_name}_detail.html")
        if not os.path.exists(template_file_path):
            with open(template_file_path, 'w') as f:
                f.write("{% extends 'base_detail.html' %}\n")
                f.write("{% block content %}\n")
                f.write(f"<!-- Template for {model_name} detail -->\n")
                f.write(f"<h1>{{{{ model|capfirst }}}} Detail</h1>\n")
                f.write("<p>ID: {{ item.id }}</p>\n")
                f.write("<p>Name: {{ item.name }}</p>\n")
                f.write("<p>Description: {{ item.description }}</p>\n")
                f.write("<!-- Add more fields here if necessary -->\n")
                f.write("{% endblock %}\n")

    def generate_form_template(self, base_template_dir, model_name):
        template_file_path = os.path.join(base_template_dir, f"{model_name}_form.html")
        if not os.path.exists(template_file_path):
            with open(template_file_path, 'w') as f:
                f.write("{% extends 'base_form.html' %}\n")
                f.write("{% block content %}\n")
                f.write(f"<!-- Template for {model_name} form -->\n")
                f.write(f"<h1>Create / Update {{ model|capfirst }}</h1>\n")
                f.write("<form method='POST'>\n")
                f.write("  {% csrf_token %}\n")
                f.write("  {{ form.as_p }}\n")
                f.write("  <button type='submit'>Save</button>\n")
                f.write("</form>\n")
                f.write("{% endblock %}\n")

    def generate_confirm_delete_template(self, base_template_dir, model_name):
        template_file_path = os.path.join(base_template_dir, f"{model_name}_confirm_delete.html")
        if not os.path.exists(template_file_path):
            with open(template_file_path, 'w') as f:
                f.write("{% extends 'base_confirm_delete.html' %}\n")
                f.write("{% block content %}\n")
                f.write(f"<!-- Template for {model_name} confirm delete -->\n")
                f.write(f"<h1>Are you sure you want to delete this {model_name}?</h1>\n")
                f.write("<form method='POST'>\n")
                f.write("  {% csrf_token %}\n")
                f.write("  <button type='submit'>Confirm Delete</button>\n")
                f.write("</form>\n")
                f.write("{% endblock %}\n")
