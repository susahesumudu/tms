from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Batch

class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_code','course' ,'description', 'created_at')
    
    # Filter the students and teachers based on their group
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        try:
            if db_field.name == 'students':
                # Only show users in the 'Student' group
                students_group = Group.objects.get(name='Student')
                kwargs['queryset'] = User.objects.filter(groups=students_group)
            if db_field.name == 'teachers':
                # Only show users in the 'Teacher' group
                teachers_group = Group.objects.get(name='Teacher')
                kwargs['queryset'] = User.objects.filter(groups=teachers_group)
        except Group.DoesNotExist:
            kwargs['queryset'] = User.objects.none()  # Empty queryset if group is missing
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
admin.site.register(Batch, BatchAdmin)
