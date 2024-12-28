# Generated by Django 5.1.4 on 2024-12-28 14:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('schedules', '0006_courseplanmodules'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseplanmodules',
            name='module',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='course_plan_moduels_modules', to='courses.module'),
            preserve_default=False,
        ),
    ]
