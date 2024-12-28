from django.views.generic import TemplateView
from django.http import Http404
from .models import CoursePlan, TrainingPlan, WeeklyPlan, LessonPlan

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server-side rendering
from django.shortcuts import render, get_object_or_404
from .models import CoursePlan, CoursePlanModules
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64

def generate_gantt_chart(request, course_plan_id):
    course_plan = get_object_or_404(CoursePlan, id=course_plan_id)
    modules = CoursePlanModules.objects.filter(course_plan=course_plan)

    if not modules:
        return render(request, 'schedule/no_modules.html', {'course_plan': course_plan})

    task_names = [module.module.module_name for module in modules]
    start_dates = [module.start_date for module in modules]
    end_dates = [module.end_date for module in modules]
    durations = [(end - start).days for start, end in zip(start_dates, end_dates)]

    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (task, start, duration) in enumerate(zip(task_names, start_dates, durations)):
        ax.barh(i, duration, left=start, align='center', edgecolor='black')

    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))
    plt.xticks(rotation=45)

    ax.set_yticks(range(len(task_names)))
    ax.set_yticklabels(task_names)
    ax.set_xlabel("Timeline")
    ax.set_ylabel("Modules")
    plt.title(f"Gantt Chart for {course_plan.course.course_name}")

    chart_buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(chart_buffer, format="png")
    plt.close(fig)
    chart_buffer.seek(0)

    gantt_chart = base64.b64encode(chart_buffer.getvalue()).decode('utf-8')

    context = {
        'course_plan': course_plan,
        'gantt_chart': gantt_chart,
    }
    return render(request, 'schedule/gantt_chart.html', context)


import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server-side rendering
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import CoursePlan, CoursePlanModules
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
import tempfile

def generate_gantt_chart_pdf(request, course_plan_id):
    # Fetch the CoursePlan object
    course_plan = get_object_or_404(CoursePlan, id=course_plan_id)
    # Fetch related modules
    modules = CoursePlanModules.objects.filter(course_plan=course_plan)

    if not modules:
        return HttpResponse("No modules found for this course plan.", status=404)

    # Prepare data for the Gantt chart
    task_names = [module.module.module_name for module in modules]
    start_dates = [module.start_date for module in modules]
    end_dates = [module.end_date for module in modules]
    durations = [(end - start).days for start, end in zip(start_dates, end_dates)]

    # Create Gantt chart
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, (task, start, duration) in enumerate(zip(task_names, start_dates, durations)):
        ax.barh(i, duration, left=start, align='center', edgecolor='black')

    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %Y'))
    plt.xticks(rotation=45)

    ax.set_yticks(range(len(task_names)))
    ax.set_yticklabels(task_names)
    ax.set_xlabel("Timeline")
    ax.set_ylabel("Modules")
    plt.title(f"Gantt Chart for {course_plan.course.course_name}")

    # Save plot to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        plt.tight_layout()
        plt.savefig(temp_file.name, format="png")
        plt.close(fig)

        # Generate PDF with Gantt chart in landscape orientation
        pdf_buffer = BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=landscape(letter))

        # Add title and details
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 550, f"Gantt Chart for {course_plan.course.course_name}")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 530, f"Coordinator: {course_plan.coordinator_name}")
        pdf.drawString(50, 510, f"Total Duration: {course_plan.total_duration} hours")
        pdf.drawString(50, 490, f"Overview: {course_plan.overview}")

        # Draw Gantt chart image
        pdf.drawImage(temp_file.name, 50, 150, width=700, height=400)

        # Finalize and close the PDF
        pdf.save()
        pdf_buffer.seek(0)

    # Return PDF as response
    response = HttpResponse(pdf_buffer, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="gantt_chart_{course_plan_id}.pdf"'
    return response



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
