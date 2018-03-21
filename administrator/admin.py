from django.contrib import admin

# Register your models here.
from administrator.models import CourseTemp


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year', 'semester', 'course_type', 'grade', 'department', 'college']


# Re-register UserAdmin
admin.site.register(CourseTemp, UserAdmin)
