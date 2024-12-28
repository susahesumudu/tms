from django.views.generic import TemplateView
from django.http import Http404
from .models import CoursePlan, TrainingPlan, WeeklyPlan, LessonPlan

class PlanBaseView(TemplateView):
    """
    A generic base view to handle plans with shared functionality.
    Subclasses must define:
    - `model`: The model to fetch the data from.
    - `template_name`: The template to render the view.
    """
    model = None  # Placeholder for the model
    object_name = None  # Placeholder for context object name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.model or not self.object_name:
            raise ValueError("Subclasses must define 'model' and 'object_name'")

        try:
            obj = self.model.objects.get(id=self.kwargs[f"{self.object_name}_id"])
            context[self.object_name] = obj
            return context
        except self.model.DoesNotExist:
            raise Http404(f"{self.model.__name__} not found.")

# Define specific views by subclassing PlanBaseView

from django.core.serializers.json import DjangoJSONEncoder
import json
from datetime import timedelta

class CoursePlanView(PlanBaseView):
    template_name = "schedule/course_plan.html"
    model = CoursePlan
    object_name = "course_plan"

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    try:
        course_plan_id = self.kwargs.get("course_plan_id")
        course_plan = CoursePlan.objects.get(id=course_plan_id)
        
        # Fetch the batch using the correct reverse relation
        batch = course_plan.course.batches.first()  # Use "batches" if related_name is set
        # OR
        # batch = course_plan.course.batch_set.first()  # Use "batch_set" if related_name is not set

        if not batch:
            raise Http404("Batch not found for this course.")

        context["course_plan"] = course_plan

        # Batch dates
        batch_start_date = batch.from_date
        batch_end_date = batch.to_date

        # Fetch modules and distribute them over the batch duration
        modules = course_plan.course.module_set.all()
        batch_duration = (batch_end_date - batch_start_date).days
        module_count = modules.count()
        module_duration = batch_duration // module_count if module_count else 0

        gantt_data = []
        current_start_date = batch_start_date

        for module in modules:
            module_end_date = current_start_date + timedelta(days=module_duration - 1)
            gantt_data.append({
                "module_name": module.module_name,
                "from_date": current_start_date.strftime("%Y-%m-%d"),
                "to_date": module_end_date.strftime("%Y-%m-%d"),
            })
            current_start_date = module_end_date + timedelta(days=1)

        context["gantt_data"] = json.dumps(gantt_data, cls=DjangoJSONEncoder)
        return context
    except CoursePlan.DoesNotExist:
        raise Http404("Course Plan not found.")


class TrainingPlanView(PlanBaseView):
    template_name = "schedule/training_plan.html"
    model = TrainingPlan
    object_name = "training_plan"

class WeeklyPlanView(PlanBaseView):
    template_name = "schedule/weekly_plan.html"
    model = WeeklyPlan
    object_name = "weekly_plan"

class LessonPlanView(PlanBaseView):
    template_name = "schedule/lesson_plan.html"
    model = LessonPlan
    object_name = "lesson_plan"
