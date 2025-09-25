# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Extended User model with role-based access
    AbstractUser gives us all default fields (username, email, password, etc.)
    We're adding our custom fields on top
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
    ]
    
    # Add custom fields
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    
    # Student-specific fields (will be None for admin users)
    roll_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    year_of_admission = models.IntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    def is_admin(self):
        """Check if user has admin role"""
        return self.role == 'admin'
    
    def is_student(self):
        """Check if user has student role"""
        return self.role == 'student'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"