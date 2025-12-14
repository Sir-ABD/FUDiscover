from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, SupervisorProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_student', 'is_supervisor', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_student', 'is_supervisor')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(StudentProfile)
admin.site.register(SupervisorProfile)
