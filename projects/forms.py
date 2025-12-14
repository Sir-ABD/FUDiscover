from django import forms
from .models import Project

class ProjectUploadForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'abstract', 'year', 'keywords', 'supervisor_name', 'document_file', 'source_code', 'github_link']
        widgets = {
            'abstract': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_document_file(self):
        file = self.cleaned_data.get('document_file')
        if file:
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed for documentation.")
        return file

    def clean_source_code(self):
        file = self.cleaned_data.get('source_code')
        if file:
            if not file.name.endswith('.zip') and not file.name.endswith('.rar'):
                raise forms.ValidationError("Only ZIP or RAR files are allowed for source code.")
        return file

    def clean(self):
        cleaned_data = super().clean()
        # Ensure either file or github link is provided? Or strictly optional?
        # User said "let it be github link or the file".
        # If they haven't provided file, they MIGHT provide github link.
        # But previously it was "optional". So if neither is provided, that's fine too.
        # However, if they provided GitHub link, we don't need file.
        return cleaned_data
