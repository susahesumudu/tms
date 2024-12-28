from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from courses.models import Course,Module,Task,  Session, Activity

from datetime import timedelta



def generate_course_plan(batch):
    course = batch.course
    start_date = batch.from_date
    course_plan = []

    for module in course.modules.all():
        module_start_date = start_date
        module_end_date = module_start_date + timedelta(weeks=module.module_duration_weeks)
        course_plan.append({
            "module_name": module.module_name,
            "module_start_date": module_start_date,
            "module_end_date": module_end_date,
        })
        start_date = module_end_date

    return course_plan

def generate_training_plan(batch):
    training_plan = []
    start_date = batch.from_date

    for module in batch.course.modules.all():
        for task in module.tasks.all():
            training_plan.append({
                "task_name": task.task_name,
                "scheduled_date": start_date,
                "duration": task.task_duration_days,
            })
            start_date += timedelta(days=task.task_duration_days)

    return training_plan

def generate_weekly_plan(batch):
    start_date = batch.from_date
    end_date = batch.to_date
    week_number = 1
    weekly_plan = []

    while start_date < end_date:
        week_end = start_date + timedelta(days=6)
        weekly_plan.append({
            "week_number": week_number,
            "start_date": start_date,
            "end_date": min(week_end, end_date),
        })
        start_date = week_end + timedelta(days=1)
        week_number += 1

    return weekly_plan


def generate_lesson_plan(session):
    activities = session.activities.all()
    return {
        "session_name": session.session_code,
        "activities": [
            {
                "activity_name": activity.activity_name,
                "activity_type": activity.activity_type,
                "duration": activity.no_of_sessions * session.session_minutes,
            }
            for activity in activities
        ],
    }

