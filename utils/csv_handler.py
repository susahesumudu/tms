import csv
import logging
from io import TextIOWrapper
from django.http import HttpResponse
from django.contrib import messages


class CSVHandler:
    """
    A reusable handler for importing and exporting data via CSV for models.
    """

    def __init__(self, model, fields, headers, foreign_key_fields=None):
        """
        Initialize the handler.

        Parameters:
            - model: The model class (e.g., Course, Module).
            - fields: A list of field names to be imported/exported.
            - headers: A list of column headers for the CSV file.
            - foreign_key_fields: A dictionary mapping field names to related models for import.
        """
        self.model = model
        self.fields = fields
        self.headers = headers
        self.foreign_key_fields = foreign_key_fields or {}

    def handle_csv(self, request, queryset=None, csv_file=None, file_name=None, action="export"):
        """
        Handle both import and export operations based on the action parameter.

        Parameters:
            - request: The current HTTP request object.
            - queryset: The queryset of the model for export.
            - csv_file: The uploaded CSV file for import.
            - file_name: The name of the CSV file for export.
            - action: The action to perform ("import" or "export").

        Returns:
            - HttpResponse for export or processes import and sends messages.
        """
        if action == "export":
            return self.export(queryset, file_name)
        elif action == "import":
            return self.import_csv(csv_file, request)
        else:
            raise ValueError("Invalid action. Use 'import' or 'export'.")

    def export(self, queryset, file_name):
        """
        Export data to a CSV file.

        Parameters:
            - queryset: The queryset of the model to export.
            - file_name: The name of the CSV file to generate.

        Returns:
            - HttpResponse containing the CSV data.
        """
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{file_name}.csv"'
        writer = csv.writer(response)

        # Write headers
        writer.writerow(self.headers)

        # Write data rows
        for obj in queryset:
            row = []
            for field in self.fields:
                value = obj
                for attr in field.split("__"):  # Handle related fields
                    value = getattr(value, attr, "")
                row.append(value)
            writer.writerow(row)

        return response

    def import_csv(self, csv_file, request):
        """
        Import data from a CSV file.

        Parameters:
            - csv_file: The uploaded CSV file.
            - request: The current request object (used for Django messages).
        """
        try:
            data = csv.reader(TextIOWrapper(csv_file, encoding='utf-8'))
            next(data)  # Skip the header row

            for row in data:
                if len(row) != len(self.fields):
                    logging.warning(f"Malformed row skipped: {row}")
                    continue

                obj_data = {}
                for index, field in enumerate(self.fields):
                    value = row[index].strip()
                    if field in self.foreign_key_fields:
                        related_model = self.foreign_key_fields[field]
                        obj_data[field] = related_model.objects.filter(**{field: value}).first()
                        if not obj_data[field]:
                            logging.warning(f"Foreign key '{field}' with value '{value}' not found. Skipping row.")
                            continue
                    else:
                        obj_data[field] = value

                # Convert numeric fields
                for key, value in obj_data.items():
                    field = self.model._meta.get_field(key)
                    if field.get_internal_type() in ("IntegerField", "FloatField"):
                        obj_data[key] = field.to_python(value)

                # Create the object
                self.model.objects.create(**obj_data)

            messages.success(request, f"{self.model.__name__}s imported successfully!")

        except Exception as e:
            logging.error(f"Error processing CSV: {str(e)}")
            messages.error(request, f"Error processing CSV: {str(e)}")
