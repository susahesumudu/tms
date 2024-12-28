import csv
from django.http import HttpResponse

class CSVExporter:
    """
    A reusable CSV Exporter class for exporting model querysets to CSV.
    """
    def __init__(self, file_name, headers, fields):
        """
        Initialize the exporter.

        Parameters:
            - file_name: The name of the CSV file to be created (without extension).
            - headers: A list of column headers for the CSV file.
            - fields: A list of fields or attributes to export from the model.
        """
        self.file_name = file_name
        self.headers = headers
        self.fields = fields

    def export(self, queryset):
        """
        Export the provided queryset to a CSV response.

        Parameters:
            - queryset: The queryset of the model to be exported.

        Returns:
            - HttpResponse containing the CSV data.
        """
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{self.file_name}.csv"'
        writer = csv.writer(response)

        # Write the headers
        writer.writerow(self.headers)

        # Write the data
        for obj in queryset:
            row = []
            for field in self.fields:
                # Handle related fields using double underscores (e.g., "course__course_name")
                value = obj
                for attr in field.split("__"):
                    value = getattr(value, attr, "")
                row.append(value)
            writer.writerow(row)

        return response
