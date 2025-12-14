from django.db import models
from django.conf import settings

class Project(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    document_file = models.FileField(upload_to='projects/documents/')
    source_code = models.FileField(upload_to='projects/code/', blank=True, null=True)
    github_link = models.URLField(blank=True, null=True, help_text="Optional: Link to GitHub repository")
    year = models.IntegerField()
    keywords = models.CharField(max_length=255, help_text="Comma-separated keywords", blank=True)
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_projects')
    supervisor_name = models.CharField(max_length=100, help_text="Name of your supervisor", blank=True)
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_projects')
    
    is_approved = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
