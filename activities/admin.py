
# Register your models here.
from django.contrib import admin

# Register your models here.from django.contrib import admin
from .models import  CommonEfficacyQuestion,Submission,GradingRubric,MarksTracker,AssessmentActivity,PracticingActivity,LearningActivity



# Custom export function for Tasks
def export_activity_to_csv(modeladmin, request, queryset):
    """
    Export selected Task records to CSV.
    """
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="activity.csv"'
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


export_activity_to_csv.short_description = "Export selected Tasks to CSV"



# Register models
admin.site.register(CommonEfficacyQuestion)



#admin.site.register(Activity)
admin.site.register(Submission)
admin.site.register(GradingRubric)
admin.site.register(MarksTracker)
admin.site.register(AssessmentActivity)
admin.site.register(PracticingActivity)
admin.site.register(LearningActivity)


