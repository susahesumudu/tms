# Generated by Django 5.1.3 on 2024-12-16 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollments', '0003_alter_batch_to_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='lock_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]