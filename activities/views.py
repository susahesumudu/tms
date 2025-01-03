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
            


from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Exercise, QuestionCompletion

class MarkQuestionCompletedView(LoginRequiredMixin, View):
    """
    Handles marking questions as completed for the logged-in user.
    """

    def post(self, request, *args, **kwargs):
        question_ids = request.POST.getlist("question_ids")
        exercise_id = request.POST.get("exercise_id")

        # Validate input
        if not question_ids or not exercise_id:
            return JsonResponse({"error": "Invalid data provided."}, status=400)

        # Fetch the exercise
        exercise = get_object_or_404(Exercise, pk=exercise_id)

        # Mark all provided questions as completed for the logged-in student
        completions = [
            QuestionCompletion(
                student=request.user,
                question_id=question_id,
                completed=True
            ) for question_id in question_ids
        ]
        
        # Bulk create or update records
        for completion in completions:
            QuestionCompletion.objects.update_or_create(
                student=completion.student,
                question=completion.question,
                defaults={"completed": completion.completed},
            )

        # Redirect back to the exercise detail page
        return redirect("activities:exercise_custom_detail", pk=exercise_id)

    def get(self, request, *args, **kwargs):
        return JsonResponse({"error": "Invalid request method."}, status=405)

from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from .models import Exercise, QuestionCompletion, Skill, Submission

class ExerciseDetailViews(DetailView):
    model = Exercise
    template_name = 'activities/exercise_detail_qiz.html'
    context_object_name = 'exercise'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exercise = self.object
        student = self.request.user

        # Fetch all questions for the exercise
        questions = exercise.questions.all().prefetch_related('skill')

        # Mark questions completed by the current student
        completed_questions = set(
            QuestionCompletion.objects.filter(
                student=student, question__exercise=exercise, completed=True
            ).values_list('question_id', flat=True)
        )
        for question in questions:
            question.completed_by_user = question.id in completed_questions

        context['questions'] = questions

        # Fetch unique skills related to the exercise
        context['skills'] = Skill.objects.filter(
            id__in=exercise.questions.values_list('skill__id', flat=True)
        ).distinct()

        # Fetch submissions for the current student
        context['submissions'] = Submission.objects.filter(exercise=exercise, student=student)

        return context



from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormView
from .models import Exercise, Submission
from .forms import SubmissionForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class SubmitExerciseView(FormView):
    template_name = 'activities/submit_exercise.html'
    form_class = SubmissionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercise'] = get_object_or_404(Exercise, id=self.kwargs['exercise_id'])
        return context

    def form_valid(self, form):
        exercise = get_object_or_404(Exercise, id=self.kwargs['exercise_id'])
        student = self.request.user

        # Prevent duplicate submissions
        if Submission.objects.filter(exercise=exercise, student=student).exists():
            return JsonResponse({"error": "Submission already exists."}, status=400)

        submission = form.save(commit=False)
        submission.exercise = exercise
        submission.student = student
        submission.save()
        return redirect('activities:exercise_custom_detail', pk=exercise.id)
