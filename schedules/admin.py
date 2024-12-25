
# Register your models here.
from django.contrib import admin
from .models import  LessonPlan, WeeklyPlan, TrainingPlan, CoursePlan


@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ('name','start_date', 'end_date', 'activity', 'no_minutes')
    search_fields = ('activity__name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    ordering = ('start_date',)

@admin.register(WeeklyPlan)
class WeeklyPlanAdmin(admin.ModelAdmin):
    list_display = ('name','start_date', 'end_date', 'task', 'no_practical_hrs', 'total_hours', 'total_minutes')
    search_fields = ('task__name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    ordering = ('start_date',)

@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = ('name','start_date', 'end_date', 'module', 'no_months')
    search_fields = ('module__name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    ordering = ('start_date',)

@admin.register(CoursePlan)
class CoursePlanAdmin(admin.ModelAdmin):
    list_display = ('name','start_date', 'end_date', 'course', 'no_months')
    search_fields = ('course__name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    ordering = ('start_date',)
