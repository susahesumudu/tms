from django.contrib import admin
from django.urls import reverse
# Register your models here.
from .models import Course, Module, Task
from django.utils.html import format_html
import csv
import logging
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from io import TextIOWrapper
from .models import Session, Activity
from utils.csv_handler import CSVHandler



class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    fields = ('module_name','module_code' ,'theory_hours', 'practical_hours', 'module_cost','module_duration_weeks')


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ('task_name', 'task_code', 'module', 'theory_hours', 'practical_hours', 'task_cost', 'task_duration_days')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_code', 'course_duration_months', 'theory_hrs', 'practical_hrs', 'course_fee', 'created_at', 'updated_at', 'delete_button')
    search_fields = ('course_name', 'course_code')
    inlines = [ModuleInline]
    list_filter = ('is_active', 'delivery_mode', 'course_mode')
    actions = ["export_csv"]

    def delete_button(self, obj):
        """
        Add a delete button for each row in the list view.
        """
        url = reverse('admin:courses_course_delete', args=[obj.id])  # Adjust 'courses_course' to match your app and model name
        return format_html('<a class="button" href="{}">Delete</a>', url)

    delete_button.short_description = "Delete"  # Column header
    delete_button.allow_tags = True

     # Define shared configuration
    csv_fields = [
        "course_name",
        "course_code",
        "theory_hrs",
        "practical_hrs",
        "course_fee",
        "course_cost",
        "no_of_batches_per_year",
        "is_active",
    ]
    csv_headers = [
        "Course Name",
        "Course Code",
        "Theory Hours",
        "Practical Hours",
        "Course Fee",
        "Course Cost",
        "Number of Batches per Year",
        "Is Active",
    ]

    def import_csv(self, request):
        if request.method == "POST":
            try:
                csv_file = request.FILES.get("csv_file")
                if not csv_file or not csv_file.name.endswith('.csv'):
                    messages.error(request, "Please upload a valid CSV file.")
                    return HttpResponseRedirect(request.path)

                handler = CSVHandler(
                    model=Course,
                    fields=self.csv_fields,
                    headers=self.csv_headers,
                )
                handler.handle_csv(request, csv_file=csv_file, action="import")
                return HttpResponseRedirect(request.path)

            except Exception as e:
                messages.error(request, f"Error importing courses: {str(e)}")
                return HttpResponseRedirect(request.path)

    def export_csv(self, request, queryset):
        handler = CSVHandler(
            model=Course,
            fields=self.csv_fields,
            headers=self.csv_headers,
        )
        return handler.handle_csv(request, queryset=queryset, file_name="courses", action="export")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv, name='course_import_csv'),
        ]
        return custom_urls + urls




@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('module_name', 'course', 'theory_hours', 'practical_hours', 'module_cost', 'delete_button')
    search_fields = ('module_name', 'course__course_name')
    inlines = [TaskInline]
    actions = []

    def delete_button(self, obj):
        url = reverse('admin:courses_module_delete', args=[obj.id])  # Adjust as necessary
        return format_html('<a class="button" href="{}">Delete</a>', url)

    delete_button.short_description = "Delete"
    delete_button.allow_tags = True

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
                    module_name, course_name, module_code, theory_hours, practical_hours, module_cost = row

                    # Fetch the related Course instance
                    course = Course.objects.filter(course_name=course_name.strip()).first()
                    if not course:
                        logging.warning(f"Course '{course_name}' not found for module: {module_name}. Skipping row.")
                        continue

                    # Create the Module instance
                    Module.objects.create(
                        course=course,
                        module_name=module_name,
                        module_code = module_code,
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



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'task_code', 'module', 'theory_hours', 'practical_hours', 'task_cost', 'task_duration_days','delete_button')
    actions = []
    list_filter = ('module',)
    search_fields = ('task_name', 'module__moduel_name')
    def delete_button(self, obj):
        url = reverse('admin:courses_task_delete', args=[obj.id])  # Adjust as necessary
        return format_html('<a class="button" href="{}">Delete</a>', url)

    delete_button.short_description = "Delete"
    delete_button.allow_tags = True

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
	    Handle the CSV file upload and import task data.
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
	                if len(row) != 7:
	                    logging.warning(f"Malformed row skipped: {row}")
	                    continue

	                task_name, task_code, module_name, theory_hours, practical_hours, task_cost, task_duration_days = row

	                module = Module.objects.filter(module_name=module_name).first()

	                if not module:
	                    logging.warning(f"Module not found for task: {task_name}. Skipping row.")
	                    continue
	                else:
	                	logging.info(f"Module found: {module_name}")

	                Task.objects.create(
	                    module=module,
	                    task_name=task_name,
	                    task_code=task_code,
	                    theory_hours=int(theory_hours),
	                    practical_hours=int(practical_hours),
	                    task_cost=float(task_cost),
	                    task_duration_days=int(task_duration_days)
	                )

	            messages.success(request, "Tasks imported successfully!")
	            # Replace 'courses' with your actual app name
	            return HttpResponseRedirect(reverse('admin:courses_task_changelist'))
	        except Exception as e:
	            logging.error(f"Error processing CSV: {str(e)}")
	            messages.error(request, f"Error processing CSV: {str(e)}")
	            return HttpResponseRedirect(request.path)

	    return render(request, 'admin/import_csv.html', {"title": "Import CSV Tasks"})




@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_type', 'session_minutes', 'session_cost',)
    search_fields = ('session_type',)
    list_filter = ('session_type',)
    ordering = ('id',)
    fields = ('session_type', 'session_minutes', 'session_cost','session_code')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    actions = []
    list_display = (
        'id',
        'activity_code',
        'activity_name',
        'task',
        'activity_type',
        'session',
        'activity_cost',
        'no_of_sessions',
        'created_at',
        'updated_at',
    )
    search_fields = ('activity_code', 'activity_name', 'task__name', 'activity_type')
    list_filter = ('activity_type', 'task', 'session')
    ordering = ('id',)
    fieldsets = (
        (None, {
            'fields': ('activity_code', 'activity_name', 'activity_type', 'task')
        }),
        ('Session Details', {
            'fields': ('session', 'no_of_sessions')
        }),
        ('Cost Details', {
            'fields': ('activity_cost',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

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
        
    def import_csv(self, request):
        if request.method == "POST":
            try:
                csv_file = request.FILES.get("csv_file")
                if not csv_file or not csv_file.name.endswith('.csv'):
                    messages.error(request, "Please upload a valid CSV file.")
                    return HttpResponseRedirect(request.path)

                data = csv.reader(TextIOWrapper(csv_file, encoding='utf-8'))
                next(data)  # Skip the header row

                for row in data:
                    # Strip whitespace and remove empty fields
                    row = [field.strip() for field in row if field.strip()]
                    
                    # Skip malformed or empty rows
                    if not row or len(row) != 6:  # Adjust column count as needed
                        logging.warning(f"Malformed row skipped: {row}, Found columns: {len(row)}")
                        continue

                    # Unpack and process the row
                    activity_name, activity_code, session_name, activity_type, activity_cost, no_of_sessions = row

                    # Fetch or create the Session instance
                    session = Session.objects.filter(name=session_name).first()
                    if not session:
                        logging.warning(f"Session '{session_name}' not found for activity: {activity_name}. Skipping row.")
                        continue

                    # Create the Activity object
                    Activity.objects.create(
                        activity_name=activity_name,
                        activity_code=activity_code,
                        session=session,
                        activity_type=activity_type,
                        activity_cost=float(activity_cost),
                        no_of_sessions=int(no_of_sessions),
                    )

                messages.success(request, "Activities imported successfully!")
                return HttpResponseRedirect(reverse('admin:courses_activity_changelist'))

            except Exception as e:
                logging.error(f"Error processing CSV: {str(e)}")
                messages.error(request, f"Error processing CSV: {str(e)}")
                return HttpResponseRedirect(request.path)

        return render(request, 'admin/import_csv.html', {"title": "Import CSV Activities"})

