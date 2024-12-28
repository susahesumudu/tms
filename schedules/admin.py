from django.contrib import admin
from .models import (
    CoursePlan,
    CoursePlanModules,
    TrainingPlan,
    TrainingPlanModule,
    TrainingPlanTask,
    WeeklyPlan,
    WeeklyTaskPlan,
    LessonPlan,
)


class CoursePlanModulesInline(admin.TabularInline):
    model = CoursePlanModules
    extra = 1


@admin.register(CoursePlan)
class CoursePlanAdmin(admin.ModelAdmin):
    list_display = ("course", "coordinator_name", "total_duration", "commencement_date", "completion_date")
    search_fields = ("course__course_name", "coordinator_name")
    list_filter = ("commencement_date", "completion_date")
    inlines = [CoursePlanModulesInline]


class TrainingPlanModuleInline(admin.TabularInline):
    model = TrainingPlanModule
    extra = 1


@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = ("course", "training_plan_title", "date_prepared", "date_revised")
    search_fields = ("course__course_name", "training_plan_title")
    list_filter = ("date_prepared", "date_revised")
    inlines = [TrainingPlanModuleInline]


class TrainingPlanTaskInline(admin.TabularInline):
    model = TrainingPlanTask
    extra = 1


@admin.register(TrainingPlanModule)
class TrainingPlanModuleAdmin(admin.ModelAdmin):
    list_display = ("training_plan", "module", "week_number")
    search_fields = ("training_plan__course__course_name", "module__module_name")
    list_filter = ("week_number",)
    inlines = [TrainingPlanTaskInline]


@admin.register(TrainingPlanTask)
class TrainingPlanTaskAdmin(admin.ModelAdmin):
    list_display = ("training_plan_module", "task", "start_date", "end_date")
    search_fields = ("training_plan_module__training_plan__course__course_name", "task__task_name")
    list_filter = ("start_date", "end_date")

class WeeklyTaskPlanInline(admin.TabularInline):
    model = WeeklyTaskPlan
    extra = 1


@admin.register(WeeklyPlan)
class WeeklyPlanAdmin(admin.ModelAdmin):
    list_display = ("course_plan_module", "module", "date_prepared", "date_revised")
    search_fields = ("course_plan_module__course_plan__course__course_name", "module__module_name")
    list_filter = ("date_prepared", "date_revised")
    inlines = [WeeklyTaskPlanInline]

@admin.register(WeeklyTaskPlan)
class WeeklyTaskPlanAdmin(admin.ModelAdmin):
    list_display = ("week_number", "task", "start_date", "end_date")
    search_fields = ("task__task_name",)
    list_filter = ("week_number", "start_date", "end_date")



@admin.register(LessonPlan)
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = (
        "module",
        "task",
        "expected_date_commencement",
        "actual_date_commencement",
        "completion_date",
        "topic_subject",
    )
    search_fields = ("module__module_name", "task__task_name", "topic_subject")
    list_filter = ("expected_date_commencement", "actual_date_commencement", "completion_date")
    filter_horizontal = ("resources",)
