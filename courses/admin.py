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




# Custom export function for Course
def export_courses_to_csv(modeladmin, request, queryset):
    """
    Export selected Course records to CSV.
    """
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="courses.csv"'
    writer = csv.writer(response)

    # Write headers
    writer.writerow([
        "Course Name",
        "Course Code",
        "Theory Hours",
        "Practical Hours",
        "Course Fee",
        "Course Cost",
        "Number of Batches per Year",
        "Is Active",
    ])

    # Write data
    for course in queryset:
        writer.writerow([
            course.course_name,
            course.course_code,
            course.theory_hrs,
            course.practical_hrs,
            course.course_fee,
            course.course_cost,
            course.no_of_batches_per_year,
            course.is_active,
        ])

    return response


export_courses_to_csv.short_description = "Export selected Courses to CSV"


# Custom export function for Modules
def export_modules_to_csv(modeladmin, request, queryset):
    """
    Export selected Module records to CSV.
    """
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="modules.csv"'
    writer = csv.writer(response)

    # Write headers
    writer.writerow([
        "Module Name",
        "Module Code",
        "Course",
        "Theory Hours",
        "Practical Hours",
        "Module Cost",
        "Module Duration Weeks",
    ])

    # Write data
    for module in queryset:
        writer.writerow([
            module.module_name,
            module.moduel_code,
            module.course.course_name,  # ForeignKey to Course
            module.theory_hours,
            module.practical_hours,
            module.module_cost,
            module.module_duration_weeks,
        ])

    return response


export_modules_to_csv.short_description = "Export selected Modules to CSV"


# Custom export function for Tasks
def export_tasks_to_csv(modeladmin, request, queryset):
    """
    Export selected Task records to CSV.
    """
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="tasks.csv"'
    writer = csv.writer(response)

    # Write headers
    writer.writerow([
        "Task Name",
        "Task Code",
        "Module",
        "Theory Hours",
        "Practical Hours",
        "Task Cost",
        "Task Duration Days",
    ])

    # Write data
    for task in queryset:
        writer.writerow([
            task.task_name,
            task.task_code,
            task.module.module_name,  # ForeignKey to Module
            task.theory_hours,
            task.practical_hours,
            task.task_cost,
            task.task_duration_days,
        ])

    return response


export_tasks_to_csv.short_description = "Export selected Tasks to CSV"


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    fields = ('module_name','moduel_code' ,'theory_hours', 'practical_hours', 'module_cost','module_duration_weeks')


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
    actions = [export_courses_to_csv]

    def delete_button(self, obj):
        """
        Add a delete button for each row in the list view.
        """
        url = reverse('admin:courses_course_delete', args=[obj.id])  # Adjust 'courses_course' to match your app and model name
        return format_html('<a class="button" href="{}">Delete</a>', url)

    delete_button.short_description = "Delete"  # Column header
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
        Handle the CSV file upload and import the data.
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
                    if len(row) != 14:
                        logging.warning(f"Malformed row skipped: {row}")
                        continue

                    course_name, course_code, duration_months, theory_hrs, practical_hrs, course_fee, \
                        module_name, module_theory_hours, module_practical_hours, module_cost, \
                        task_name, task_theory_hours, task_practical_hours, task_cost = row

                    course, created = Course.objects.get_or_create(
                        course_name=course_name,
                        course_code=course_code,
                        defaults={
                            "duration_months": int(duration_months),
                            "theory_hours": int(theory_hrs),
                            "practical_hours": int(practical_hrs),
                            "course_fee": float(course_fee)
                        }
                    )

                    logging.debug(f"Course {'created' if created else 'retrieved'}: {course}")

                    module, created = Module.objects.get_or_create(
                        course=course,
                        module_name=module_name,
                        defaults={
                            "theory_hours": int(module_theory_hours),
                            "practical_hours": int(module_practical_hours),
                            "module_cost": float(module_cost)
                        }
                    )

                    logging.debug(f"Module {'created' if created else 'retrieved'}: {module}")

                    task = Task.objects.create(
                        module=module,
                        task_name=task_name,
                        theory_hours=int(task_theory_hours),
                        practical_hours=int(task_practical_hours),
                        task_cost=float(task_cost)
                    )

                    logging.debug(f"Task created: {task}")

                messages.success(request, "CSV imported successfully!")
                return HttpResponseRedirect(reverse('admin:courses_course_changelist'))
            except Exception as e:
                logging.error(f"Error processing CSV: {str(e)}")
                messages.error(request, f"Error processing CSV: {str(e)}")
                return HttpResponseRedirect(request.path)

        return render(request, 'admin/import_csv.html', {"title": "Import CSV"})


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('module_name', 'course', 'theory_hours', 'practical_hours', 'module_cost', 'delete_button')
    search_fields = ('module_name', 'course__course_name')
    inlines = [TaskInline]
    actions = [export_modules_to_csv]

    def delete_button(self, obj):
        url = reverse('admin:courses_module_delete', args=[obj.id])  # Adjust as necessary
        return format_html('<a class="button" href="{}">Delete</a>', url)

    delete_button.short_description = "Delete"
    delete_button.allow_tags = True


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'task_code', 'module', 'theory_hours', 'practical_hours', 'task_cost', 'task_duration_days','delete_button')
    actions = [export_tasks_to_csv]
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
    list_display = ('id', 'session_type', 'session_minutes', 'session_cost')
    search_fields = ('session_type',)
    list_filter = ('session_type',)
    ordering = ('id',)
    fields = ('session_type', 'session_minutes', 'session_cost')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
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