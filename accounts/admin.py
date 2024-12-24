# admin.py
from django.contrib import admin
from .models import  StudentProfile ,TeacherProfile,StaffProfile,ParentProfile


admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(StaffProfile)
admin.site.register(ParentProfile)

