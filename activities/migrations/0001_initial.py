# Generated by Django 5.1.4 on 2024-12-26 16:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0005_alter_session_session_cost'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MainActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_name', models.CharField(max_length=100)),
                ('activity_code', models.CharField(max_length=10)),
                ('description', models.TextField()),
                ('mode', models.CharField(choices=[('Online', 'Online'), ('Video', 'Video'), ('Physical', 'Physical')], max_length=10)),
                ('minutes', models.FloatField()),
                ('deadline', models.DateTimeField()),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_activity', to='courses.activity')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_session', to='courses.session')),
            ],
        ),
        migrations.CreateModel(
            name='CommonEfficacyQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='GradingRubric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criteria', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('max_points', models.FloatField()),
                ('points_awarded', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssessmentActivity',
            fields=[
                ('mainactivity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activities.mainactivity')),
                ('assessment_type', models.CharField(choices=[('MCQ', 'MCQ'), ('Presentation', 'Presentation'), ('Project', 'Project'), ('Demonstration', 'Demonstration'), ('Assingment', 'Assingment')], max_length=100)),
                ('max_marks', models.FloatField()),
            ],
            bases=('activities.mainactivity',),
        ),
        migrations.CreateModel(
            name='LearningActivity',
            fields=[
                ('mainactivity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activities.mainactivity')),
                ('learning_goal', models.TextField()),
                ('is_required', models.BooleanField(default=True)),
            ],
            bases=('activities.mainactivity',),
        ),
        migrations.CreateModel(
            name='PracticingActivity',
            fields=[
                ('mainactivity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='activities.mainactivity')),
                ('practice_type', models.CharField(max_length=100)),
                ('is_assessment_related', models.BooleanField(default=False)),
            ],
            bases=('activities.mainactivity',),
        ),
        migrations.AddField(
            model_name='mainactivity',
            name='efficacy_questions',
            field=models.ManyToManyField(blank=True, to='activities.commonefficacyquestion'),
        ),
        migrations.CreateModel(
            name='MarksTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_marks', models.FloatField(default=0.0)),
                ('weekly_marks', models.FloatField(default=0.0)),
                ('monthly_marks', models.FloatField(default=0.0)),
                ('course_wise_marks', models.FloatField(default=0.0)),
                ('final_grade', models.CharField(max_length=10)),
                ('final_assessment_score', models.FloatField(blank=True, null=True)),
                ('tasks_completed', models.IntegerField(default=0)),
                ('exercises_completed', models.IntegerField(default=0)),
                ('on_time_completion', models.BooleanField(default=False)),
                ('practical_hours', models.FloatField(default=0.0)),
                ('theory_hours', models.FloatField(default=0.0)),
                ('num_of_prev_attempts', models.IntegerField(default=0)),
                ('industry_training_experience', models.FloatField(default=0.0)),
                ('students', models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'Student'}, on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_file', models.FileField(upload_to='submissions/')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('marks', models.FloatField(blank=True, null=True)),
                ('feedback', models.TextField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('on_time_completion', models.BooleanField(default=False)),
                ('marks_awarded', models.FloatField(default=0.0)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='courses.activity')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
