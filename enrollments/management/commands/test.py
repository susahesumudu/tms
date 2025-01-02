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

    def write_template(self, path, content):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as template_file:
            template_file.write(content)
