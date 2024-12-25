# Generated by Django 5.1.4 on 2024-12-25 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_session_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='session_type',
            field=models.CharField(choices=[('Knowledge-Based', 'Knowledge-Based'), ('Hands-On', 'Hands-On'), ('Integrated', 'Integrated')], help_text='Knowledge-Based: Theoretical, Hands-On: Practical, Integrated: Both Theoretical and Practical', max_length=50),
        ),
    ]