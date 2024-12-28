    def get_urls(self):
            urls = super().get_urls()
            custom_urls = [
                path('import-csv/', self.import_csv, name='import_csv'),
            ]
            return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        """
        Add an "Upload CSV" button above the admin list.
        """
        extra_context = extra_context or {}
        extra_context['upload_csv_url'] = reverse('admin:import_csv')
        return super().changelist_view(request, extra_context=extra_context)
    
   
    logging.basicConfig(level=logging.DEBUG)

    def import_csv(self, request):
        """
        Handle the CSV file upload and import module data.
        """
        if request.method == "POST":
            try:
                csv_file = request.FILES.get("csv_file")
                if not csv_file or not csv_file.name.endswith('.csv'):
                    messages.error(request, "Please upload a valid CSV file.")
                    return HttpResponseRedirect(request.path)

                data = csv.reader(TextIOWrapper(csv_file, encoding='utf-8'))
                next(data)  # Skip the header row

                for row in data:
                    # Ensure the row has the correct number of columns
                    if len(row) != 5:  # Adjust based on your module data
                        logging.warning(f"Malformed row skipped: {row}")
                        continue

                    # Unpack the row data
                    module_name, course_name, moduel_code, theory_hours, practical_hours, module_cost = row

                    # Fetch the related Course instance
                    course = Course.objects.filter(course_name=course_name.strip()).first()
                    if not course:
                        logging.warning(f"Course '{course_name}' not found for module: {module_name}. Skipping row.")
                        continue

                    # Create the Module instance
                    Module.objects.create(
                        course=course,
                        module_name=module_name,
                        module_code = moduel_code,
                        theory_hours=theory_hours,
                        practical_hours=practical_hours,
                        module_cost=module_cost,
                        module_duration_weeks=int(module_duration_weeks),
                    )

                messages.success(request, "Modules imported successfully!")
                return HttpResponseRedirect(reverse('admin:courses_module_changelist'))

            except Exception as e:
                logging.error(f"Error processing CSV: {str(e)}")
                messages.error(request, f"Error processing CSV: {str(e)}")
                return HttpResponseRedirect(request.path)

        return render(request, 'admin/import_csv.html', {"title": "Import CSV Modules"})
