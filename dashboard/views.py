from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

from accounts.models import StudentProfile, TeacherProfile
from courses.models import Activity
from activities.models import MarksTracker, Quiz, Exercise, QuizSubmission, Submission
from .forms import AssignExerciseForm, AssignQuizForm

class DashboardRedirectView(LoginRequiredMixin, TemplateView):
    """Redirect users to their role-specific dashboard."""
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name='Teacher').exists():
            return redirect('teacher_dashboard')
        elif user.groups.filter(name='Student').exists():
            return redirect('student_dashboard')
        elif user.groups.filter(name='Admin').exists() or user.is_superuser:
            return redirect('/admin/')
        return redirect('default_dashboard')  # Fallback


 



from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from activities.models import QuizSubmission, Submission

class TeacherDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/teacher_dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch submitted but ungraded quizzes and exercises
        ungraded_quizzes = QuizSubmission.objects.filter(score__isnull=True, quiz_is_completed=True)
        ungraded_exercises = Submission.objects.filter(score__isnull=True, exercise_is_completed=True)

        # Pass the ungraded submissions to the template
        context['ungraded_quizzes'] = ungraded_quizzes
        context['ungraded_exercises'] = ungraded_exercises
        return context



class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/student_dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the student's marks tracker
        marks_tracker, created = MarksTracker.objects.get_or_create(student=self.request.user)

        # Fetch quizzes assigned and completed
        quiz_submissions = QuizSubmission.objects.filter(student=self.request.user)

        # Fetch exercises assigned and completed
        exercise_submissions = Submission.objects.filter(student=self.request.user)

        # Calculate statistics
        total_quizzes = quiz_submissions.count()
        completed_quizzes = quiz_submissions.filter(quiz_is_completed=True).count()

        total_exercises = exercise_submissions.count()
        completed_exercises = exercise_submissions.filter(exercise_is_completed=True).count()

        on_time_quizzes = quiz_submissions.filter(is_ontime_completed=True).count()
        on_time_exercises = exercise_submissions.filter(is_ontime_completed=True).count()

        # Add details to the context
        context.update({
            'marks_tracker': marks_tracker,
            'quiz_submissions': quiz_submissions,
            'exercise_submissions': exercise_submissions,
            'total_quizzes': total_quizzes,
            'completed_quizzes': completed_quizzes,
            'on_time_quizzes': on_time_quizzes,
            'total_exercises': total_exercises,
            'completed_exercises': completed_exercises,
            'on_time_exercises': on_time_exercises,
        })

        return context


class StaffDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/staff_dashboard.html'


class ParentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/parent_dashboard.html'
  

