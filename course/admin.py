from django.contrib import admin

# Register your models here.


from .models import Course

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'year', 'semester', 'course_type', 'grade', 'department', 'college']


# Re-register UserAdmin
admin.site.register(Course, UserAdmin)
