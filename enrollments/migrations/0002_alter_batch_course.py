# Generated by Django 5.1.4 on 2024-12-28 13:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('enrollments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='courses.course'),
        ),
    ]