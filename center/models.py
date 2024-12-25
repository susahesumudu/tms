from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def validate_pdf_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")


class TrainingCenter(models.Model):
    center_name = models.CharField(
        max_length=200,
        help_text="Name of the training center.",
        verbose_name="Training Center Name"
    )
    address = models.TextField(
        help_text="Address of the training center.",
        verbose_name="Address"
    )
    contact_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Contact number of the training center.",
        verbose_name="Contact Number"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Email address of the training center.",
        verbose_name="Email Address"
    )
    registration_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique registration number of the training center.",
        verbose_name="Registration Number"
    )
    established_date = models.DateField(
        blank=True,
        null=True,
        help_text="Date when the training center was established.",
        verbose_name="Established Date"
    )
    head_of_center = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Name of the head of the training center.",
        verbose_name="Head of Center"
    )
    total_capacity = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Total capacity of trainees the center can accommodate.",
        verbose_name="Total Capacity"
    )
    specialization = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Specialization or focus area of the training center.",
        verbose_name="Specialization"
    )
    contact_person = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Contact person for inquiries.",
        verbose_name="Contact Person"
    )
    business_reg_no = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Business Registration Number.",
        verbose_name="Business Registration Number"
    )
    business_reg_copy = models.FileField(
        upload_to='br/',
        blank=True,
        null=True,
        validators=[validate_pdf_extension],
        verbose_name="Business Registration Copy (PDF)",
        help_text="Upload the business registration copy as a PDF file."
    )
    tvec_reg_copy = models.FileField(
        upload_to='br/',
        blank=True,
        null=True,
        validators=[validate_pdf_extension],
        verbose_name="TVEC Registration Copy  (PDF)",
        help_text="Upload the TVEC registration copy  a PDF file."
    )
   
    

    def __str__(self):
        return self.center_name