from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.apps import apps


# Base CRUD view classes
class BaseListView(ListView):
    context_object_name = 'items'

    def get_queryset(self):
        model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
        return model.objects.all()

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_list.html"]


class BaseDetailView(DetailView):
    context_object_name = 'item'

    def get_object(self):
        model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
        return model.objects.get(pk=self.kwargs['pk'])

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_detail.html"]


class BaseCreateView(CreateView):
    fields = '__all__'

    def get_queryset(self):
        model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
        return model.objects.all()

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_form.html"]

    def get_success_url(self):
            return reverse_lazy(f"{self.kwargs['app_name']}:{self.kwargs['model'].lower()}_list")


class BaseUpdateView(UpdateView):
    fields = '__all__'

    def get_object(self):
        model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
        return model.objects.get(pk=self.kwargs['pk'])

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_form.html"]

    def get_success_url(self):
            return reverse_lazy(f"{self.kwargs['app_name']}:{self.kwargs['model'].lower()}_list")


class BaseDeleteView(DeleteView):

    def get_object(self):
        model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
        return model.objects.get(pk=self.kwargs['pk'])

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_confirm_delete.html"]

    def get_success_url(self):
            return reverse_lazy(f"{self.kwargs['app_name']}:{self.kwargs['model'].lower()}_list")
            



from .models import *

class ExerciseDetailView(DetailView):
    model = Exercise
    template_name = 'activities/exercise_detail_qiz.html'
    context_object_name = 'exercise'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the current exercise
        exercise = self.object

        # Get related questions
        context['questions'] = exercise.questions.all()  # Use related_name 'questions'

        # Get unique skills associated with all questions of this exercise
        context['skills'] = Skill.objects.filter(question_skills__exercise=exercise).distinct()

        # Get submissions related to this exercise
        context['submissions'] = Submission.objects.filter(exercise=exercise)

        return context
