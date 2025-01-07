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
        return model.objects.get(slug=self.kwargs['slug'])

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
        return model.objects.get(slug=self.kwargs['slug'])

    def get_template_names(self):
        return [f"{self.kwargs['app_name']}/{self.kwargs['model'].lower()}_form.html"]

    def get_success_url(self):
        return reverse_lazy(f"{self.kwargs['app_name']}:{self.kwargs['model'].lower()}_list")


class BaseDeleteView(DeleteView):

    def get_object(self):
        model = apps.get_model(app_label=self.kwargs['app_name'], model_name=self.kwargs['model'])
        return model.objects.get(slug=self.kwargs['slug'])

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

class ExerciseDetailViews(LoginRequiredMixin,DetailView):
    model = Exercise
    template_name = 'activities/exercise_detail_qiz.html'
    context_object_name = 'exercise'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exercise = self.object
        user = self.request.user

        # Debugging log
        logger.debug(f"User: {user.username}, Is teacher: {user.groups.filter(name='Teacher').exists()}")

        # Check if the user is a teacher
        is_teacher = user.groups.filter(name="Teacher")
        context['is_teachers'] = is_teacher

        # Fetch all questions for the exercise
        questions = exercise.questions.all().prefetch_related('skill')

        if not is_teacher:
            # Fetch IDs of completed questions for the current student
            completed_question_ids = set(
                QuestionCompletion.objects.filter(
                    student=user, question__exercise=exercise, completed=True
                ).values_list('question_id', flat=True)
            )
            # Annotate questions with a completion flag for the student
            for question in questions:
                question.completed_by_user = question.id in completed_question_ids
            logger.debug(f"Completed questions for user {user.username}: {completed_question_ids}")
        else:
            # Teachers do not need individual completion tracking
            for question in questions:
                question.completed_by_user = False

        context['questions'] = questions

        # Fetch unique skills related to the exercise
        skill_ids = questions.values_list('skill__id', flat=True)
        context['skills'] = Skill.objects.filter(id__in=skill_ids).distinct()

        logger.debug(f"Skills for exercise {exercise.id}: {skill_ids}")

        # Fetch submissions
        if is_teacher:
            # Teachers get all submissions for the exercise
            context['submissions'] = Submission.objects.filter(exercise=exercise)
            logger.debug(f"Submissions fetched for teacher {user.username}")
        else:
            # Students get only their submissions
            context['submissions'] = Submission.objects.filter(exercise=exercise, student=user)
            logger.debug(f"Submissions fetched for student {user.username}")

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


from courses.models import Activity

from django.http import Http404

from django.shortcuts import get_object_or_404

from .models import  Exercise

class ActivityExerciseListView(LoginRequiredMixin, ListView):
    model = Exercise
    template_name = 'activities/activity_exercises_list.html'
    context_object_name = 'exercises'

    def get_queryset(self):
        # Use slug to get the activity
        activity = get_object_or_404(Activity, slug=self.kwargs['slug'])
        return Exercise.objects.filter(activity=activity)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Include activity details in the context using slug
        context['activity'] = get_object_or_404(Activity, slug=self.kwargs['slug'])
        context['column_count'] = 10  # Adjust based on your table's column count
        print("Context Data:", context)  # Debugging: Print context data
        return context




from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Exercise, Skill, Submission, Activity
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Exercise, Skill, Submission

class ActivityExerciseDetailView(LoginRequiredMixin, DetailView):
    model = Exercise
    template_name = 'activities/activity_exercises_detail.html'
    context_object_name = 'exercise'

    def get_object(self):
        """Fetch Exercise based on slug."""
        slug = self.kwargs.get('slug')
        print(f"Fetching Exercise for slug={slug}")  # Debugging
        return get_object_or_404(Exercise, slug=slug)

    def get_context_data(self, **kwargs):
        """Add questions and other relevant context to the template."""
        context = super().get_context_data(**kwargs)
        exercise = self.object
        user = self.request.user

        # Check if the user belongs to the "Teacher" group
        is_teacher = user.groups.filter(name="Teacher").exists()

        # Fetch all questions for the exercise and prefetch related skills
        questions = exercise.questions.prefetch_related('skill')

        # Collect skill IDs from all questions
        skill_ids = set(
            skill.id for question in questions for skill in question.skill.all()
        )

        # Add data to context
        context['is_teacher'] = is_teacher
        context['questions'] = questions
        context['skills'] = Skill.objects.filter(id__in=skill_ids).distinct()
        context['submissions'] = Submission.objects.filter(exercise=exercise, student=self.request.user)

        return context


from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Question, Exercise

class ActivityExerciseAddQuestion(LoginRequiredMixin, CreateView):
    model = Question
    template_name = 'activities/exercise_question_add.html'
    fields = ['text', 'weighting', 'tutorial_url', 'video_url', 'skill']  # Fields to display in the form

    def form_valid(self, form):
        # Associate the question with the exercise based on the slug
        slug = self.kwargs['slug']
        exercise = get_object_or_404(Exercise, slug=slug)
        form.instance.exercise = exercise
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Add the exercise to the context for display in the template
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['exercise'] = get_object_or_404(Exercise, slug=slug)
        return context

    def get_success_url(self):
        # Redirect to the exercise details page after adding a question
        return reverse_lazy('activities:exercise_detail_questions', kwargs={'slug': self.kwargs['slug']})
