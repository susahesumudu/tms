# Generated by Django 5.1.4 on 2024-12-28 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_name', models.CharField(help_text='Name or type of the resource.', max_length=100, verbose_name='Resource Name')),
                ('resource_type', models.CharField(choices=[('Computer', 'Computer'), ('Printer', 'Printer'), ('Projector', 'Projector'), ('Furniture', 'Furniture'), ('Other', 'Other')], help_text='Type of the resource.', max_length=50, verbose_name='Resource Type')),
                ('quantity', models.PositiveIntegerField(help_text='Number of this type of resource available.', verbose_name='Quantity')),
                ('description', models.TextField(blank=True, help_text='Additional details about the resource.', null=True, verbose_name='Description')),
                ('date_acquired', models.DateField(blank=True, help_text='Date the resource was acquired.', null=True, verbose_name='Date Acquired')),
                ('training_center', models.ForeignKey(help_text='The training center to which this resource belongs.', on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='center.trainingcenter', verbose_name='Training Center')),
            ],
        ),
    ]