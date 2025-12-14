from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm # Or custom form dealing with custom user
from .models import User, StudentProfile, SupervisorProfile
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Unified Registration Form
class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('supervisor', 'Supervisor'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, initial='student')
    
    # Student Fields
    reg_no = forms.CharField(max_length=20, required=False, label="Registration Number")
    graduation_year = forms.IntegerField(required=False, label="Graduation Year")
    
    # Supervisor Fields
    department = forms.CharField(max_length=100, required=False, label="Department")
    staff_id = forms.CharField(max_length=20, required=False, label="Staff ID")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        
        if role == 'student':
            if not cleaned_data.get('reg_no'):
                self.add_error('reg_no', 'This field is required for students.')
            if not cleaned_data.get('graduation_year'):
                self.add_error('graduation_year', 'This field is required for students.')
            # Check uniqueness
            if StudentProfile.objects.filter(reg_no=cleaned_data.get('reg_no')).exists():
                self.add_error('reg_no', 'This Registration Number is already registered.')
                
        elif role == 'supervisor':
            if not cleaned_data.get('department'):
                self.add_error('department', 'This field is required for supervisors.')
            if not cleaned_data.get('staff_id'):
                self.add_error('staff_id', 'This field is required for supervisors.')
            # Check uniqueness
            if SupervisorProfile.objects.filter(staff_id=cleaned_data.get('staff_id')).exists():
                self.add_error('staff_id', 'This Staff ID is already registered.')
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        
        if role == 'student':
            user.is_student = True
        elif role == 'supervisor':
            user.is_supervisor = True
            
        if commit:
            user.save()
            if role == 'student':
                StudentProfile.objects.create(
                    user=user, 
                    reg_no=self.cleaned_data['reg_no'],
                    graduation_year=self.cleaned_data['graduation_year']
                )
            elif role == 'supervisor':
                SupervisorProfile.objects.create(
                    user=user,
                    department=self.cleaned_data['department'],
                    staff_id=self.cleaned_data['staff_id']
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
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('project_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
