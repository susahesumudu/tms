from django.contrib import admin
from .models import Exercise, Question, Skill, Quiz,Submission,Choice,QuizSubmission,GradingRubric,QuizQuestion

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity', 'difficulty_level', 'max_score',  'created_at')
    list_filter = ('difficulty_level', 'activity')
    search_fields = ('title', 'description', 'activity__name')

    def get_deadline(self, obj):
        return obj.deadline
    get_deadline.short_description = 'Deadline'


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'activity', 'max_score', 'created_at')
    list_filter = ('activity', 'created_at')
    search_fields = ('title', 'description', 'activity__name')

    def get_deadline(self, obj):
        return obj.deadline
    get_deadline.short_description = 'Deadline'

admin.site.register(Submission)
admin.site.register(QuizSubmission)

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Skill)
admin.site.register(GradingRubric)
admin.site.register(QuizQuestion)

