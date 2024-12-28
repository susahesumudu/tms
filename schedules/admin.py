from django.contrib import admin
from schedules.models import CoursePlan, TrainingPlan, WeeklyPlan, LessonPlan,CoursePlanModules

# Base Admin Configuration for Shared Features
class PlanBaseAdmin(admin.ModelAdmin):
    list_display = ("date_prepared",)
    search_fields = ("date_prepared",)
    list_filter = ("date_prepared",)
    date_hierarchy = "date_prepared"

# Course Plan Admin
@admin.register(CoursePlan)
class CoursePlanAdmin(PlanBaseAdmin):
    list_display = PlanBaseAdmin.list_display + ("course", "coordinator_name", "commencement_date", "completion_date")
    search_fields = PlanBaseAdmin.search_fields + ("course__course_name", "coordinator_name")
    list_filter = PlanBaseAdmin.list_filter + ("commencement_date", "completion_date")

@admin.register(CoursePlanModules)
class CoursePlanModules(admin.ModelAdmin):
    list_display = ('course_plan','start_date','end_date')
    


# Training Plan Admin
@admin.register(TrainingPlan)
class TrainingPlanAdmin(PlanBaseAdmin):
    list_display = PlanBaseAdmin.list_display + ("module", "occupation", "week_number", "date_revised")
    search_fields = PlanBaseAdmin.search_fields + ("module__module_name", "occupation")
    list_filter = PlanBaseAdmin.list_filter + ("week_number", "date_revised")

# Weekly Plan Admin
@admin.register(WeeklyPlan)
class WeeklyPlanAdmin(PlanBaseAdmin):
    list_display = PlanBaseAdmin.list_display + ("course_plan", "week_number", "start_date", "end_date")
    search_fields = PlanBaseAdmin.search_fields + ("course_plan__course__course_name", "week_number")
    list_filter = PlanBaseAdmin.list_filter + ("start_date", "end_date")
    filter_horizontal = ("modules_covered",)

# Lesson Plan Admin
@admin.register(LessonPlan)
class LessonPlanAdmin(PlanBaseAdmin):
    list_display = PlanBaseAdmin.list_display + ("module", "task", "trade_subject", "expected_date_commencement", "completion_date")
    search_fields = PlanBaseAdmin.search_fields + ("module__module_name", "task__task_name", "trade_subject")
    list_filter = PlanBaseAdmin.list_filter + ("expected_date_commencement", "completion_date")
