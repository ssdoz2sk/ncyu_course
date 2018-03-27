from django.contrib import admin

# Register your models here.


from .models import CourseUser

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'email']


# Re-register UserAdmin
admin.site.register(CourseUser, UserAdmin)
