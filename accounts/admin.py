# admin.py
from django.contrib import admin
from .models import  StudentProfile ,TeacherProfile,StaffProfile,ParentProfile



admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(StaffProfile)
admin.site.register(ParentProfile)

from django.contrib import admin
from .models import ClickLog

@admin.register(ClickLog)
class ClickLogAdmin(admin.ModelAdmin):
    list_display = ('url', 'element_id', 'element_tag', 'timestamp', 'ip_address', 'user')
    list_filter = ('timestamp', 'url')
    search_fields = ('url', 'element_id', 'user_agent')
