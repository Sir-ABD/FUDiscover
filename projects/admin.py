from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'year', 'is_approved', 'uploaded_at')
    list_filter = ('year', 'is_approved')
    search_fields = ('title', 'abstract', 'student__username')
