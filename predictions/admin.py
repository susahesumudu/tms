from django.contrib import admin

# # Register your models here.
# from django.contrib import admin

# from django.contrib import admin
# from .models import Student, Resource, Course, Interaction

# admin.site.register(Student)
# admin.site.register(Resource)
# admin.site.register(Course)


# class InteractionAdmin(admin.ModelAdmin):
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "student":
#             kwargs["queryset"] = User.objects.filter(groups__name="Student")
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)

# admin.site.register(Interaction, InteractionAdmin)
