from django.contrib import admin
from django.urls import reverse
from django import forms
from .models import TrainingCenter
from django.shortcuts import render
from django.urls import path




@admin.register(TrainingCenter)

class TrainingCenterAdmin(admin.ModelAdmin):

    list_display = ('center_name', 'registration_number', 'contact_number', 'email', 'total_capacity')
    search_fields = ('center_name', 'registration_number', 'specialization')
    list_filter = ('established_date', 'specialization')
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('test_cbt/', self.test_cbt, name='test_cbt'),
        ]
        return custom_urls + urls
    
    def changelist_view(self, request, extra_context=None):
        """
        Add an "Upload CSV" button above the admin list.
        """
        extra_context = extra_context or {}
        extra_context['test_url'] = reverse('admin:test_cbt')
        return super().changelist_view(request, extra_context=extra_context)

    def test_cbt(self, request):
        return render(request, 'admin/test.html', {"title": "Test"})


from .models import Resource

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('resource_name', 'resource_type', 'training_center', 'quantity', 'date_acquired')
    list_filter = ('resource_type', 'training_center', 'date_acquired')
    search_fields = ('resource_name', 'description', 'training_center__center_name')
    ordering = ('training_center', 'resource_name')
    fieldsets = (
        (None, {
            'fields': ('training_center', 'resource_name', 'resource_type', 'quantity')
        }),
        ('Additional Information', {
            'fields': ('description', 'date_acquired'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(Resource, ResourceAdmin)