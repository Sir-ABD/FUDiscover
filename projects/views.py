from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Project
from .forms import ProjectUploadForm
from .utils import check_title_similarity, check_abstract_similarity

def project_list(request):
    query = request.GET.get('q')
    projects = Project.objects.filter(is_approved=True).order_by('-year')

    if query:
        # SQLite compatible search (icontains)
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(abstract__icontains=query) |
            Q(student__username__icontains=query) | 
            Q(year__icontains=query) |
            Q(keywords__icontains=query) |
            Q(supervisor_name__icontains=query)
        )

    return render(request, 'projects/project_list.html', {'projects': projects, 'query': query})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # Only allow viewing details if approved or user is the owner or supervisor/admin
    if not project.is_approved:
        if request.user != project.student and not request.user.is_staff and not request.user.is_superuser:
             messages.error(request, "This project is not yet approved.")
             return redirect('project_list')
             
    return render(request, 'projects/project_detail.html', {'project': project})

@login_required
def upload_project(request):
    if not request.user.is_student: 
        # Optional: restrict to students only
        pass

    if request.method == 'POST':
        form = ProjectUploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            abstract = form.cleaned_data['abstract']

            # Plagiarism Check
            title_exists, similar_title = check_title_similarity(title)
            if title_exists:
                messages.error(request, f"Possible Plagiarism: Title is too similar to existing project '{similar_title}'.")
                return render(request, 'projects/upload_project.html', {'form': form})

            abstract_exists, similar_proj_title = check_abstract_similarity(abstract)
            if abstract_exists:
                messages.error(request, f"Possible Plagiarism: Abstract content overlaps significantly with '{similar_proj_title}'.")
                return render(request, 'projects/upload_project.html', {'form': form})

            project = form.save(commit=False)
            project.student = request.user
            project.save()
            messages.success(request, "Project uploaded successfully! Waiting for supervisor approval.")
            return redirect('project_list')
    else:
        form = ProjectUploadForm()
    
    return render(request, 'projects/upload_project.html', {'form': form})
