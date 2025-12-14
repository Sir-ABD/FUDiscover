from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    reg_no = models.CharField(max_length=20, unique=True, help_text="Registration Number")
    graduation_year = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.reg_no}"

class SupervisorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supervisor_profile')
    department = models.CharField(max_length=100)
    staff_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.staff_id}"
