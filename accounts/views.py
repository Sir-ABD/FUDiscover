from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm # Or custom form dealing with custom user
from .models import User, StudentProfile
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Simple Custom Registration Form
class StudentRegistrationForm(UserCreationForm):
    reg_no = forms.CharField(max_length=20, required=True)
    graduation_year = forms.IntegerField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user, 
                reg_no=self.cleaned_data['reg_no'],
                graduation_year=self.cleaned_data['graduation_year']
            )
        return user

@login_required
def profile(request):
    user = request.user
    projects = []
    if user.is_student:
        projects = user.submitted_projects.all()
    elif user.is_supervisor:
        projects = user.supervised_projects.all()
    
    return render(request, 'accounts/profile.html', {'user': user, 'projects': projects})

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('project_list')
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
