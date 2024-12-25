# Generated by Django 5.1.4 on 2024-12-25 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('center', '0002_trainingcenter_br_no_trainingcenter_contact_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainingcenter',
            name='br_no',
        ),
        migrations.AddField(
            model_name='trainingcenter',
            name='business_reg_copy',
            field=models.ImageField(blank=True, null=True, upload_to='br/'),
        ),
        migrations.AddField(
            model_name='trainingcenter',
            name='business_reg_no',
            field=models.CharField(blank=True, help_text='Bussiness Registraiton Number', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='trainingcenter',
            name='tvec_reg_copy',
            field=models.ImageField(blank=True, null=True, upload_to='tvec/'),
        ),
    ]
