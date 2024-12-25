from django.contrib import admin
from django.urls import reverse
# Register your models here.
from .models import Course, Module, Task
from django.utils.html import format_html
class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    fields = ('module_name','moduel_code' ,'theory_hours', 'practical_hours', 'module_cost','module_duration_weeks')


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ('task_name', 'theory_hours', 'practical_hours', 'task_cost')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_code', 'course_duration_months', 'theory_hrs', 'practical_hrs', 'course_fee', 'created_at', 'updated_at', 'delete_button')
    search_fields = ('course_name', 'course_code')
    inlines = [ModuleInline]
    list_filter = ('is_active', 'delivery_mode', 'course_mode')

    def delete_button(self, obj):
        """
        Add a delete button for each row in the list view.
        """
        url = reverse('admin:courses_course_delete', args=[obj.id])  # Adjust 'courses_course' to match your app and model name
        return format_html('<a class="button" href="{}">Delete</a>', url)

    delete_button.short_description = "Delete"  # Column header
    delete_button.allow_tags = True


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('module_name', 'course', 'theory_hours', 'practical_hours', 'module_cost', 'delete_button')
    search_fields = ('module_name', 'course__course_name')
    inlines = [TaskInline]

    def delete_button(self, obj):
        url = reverse('admin:courses_module_delete', args=[obj.id])  # Adjust as necessary
        return format_html('<a class="button" href="{}">Delete</a>', url)

    delete_button.short_description = "Delete"
    delete_button.allow_tags = True


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'task_code', 'module', 'theory_hours', 'practical_hours', 'task_cost', 'delete_button')
    list_filter = ('module',)
    search_fields = ('task_name', 'module__moduel_name')
    def delete_button(self, obj):
        url = reverse('admin:courses_task_delete', args=[obj.id])  # Adjust as necessary
        return format_html('<a class="button" href="{}">Delete</a>', url)

    delete_button.short_description = "Delete"
    delete_button.allow_tags = True