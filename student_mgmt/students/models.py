# students/models.py
from django.db import models
from django.conf import settings
from django.urls import reverse

class Student(models.Model):
    """
    Student model to store academic information
    Linked to User model via OneToOneField for authentication
    """
    # Link to our custom User model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    
    # Academic Information
    student_id = models.CharField(max_length=20, unique=True, help_text="Unique student ID")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    # Academic Details
    department = models.CharField(max_length=100)
    year_of_admission = models.IntegerField()
    current_semester = models.IntegerField(default=1)
    
    # Personal Information
    date_of_birth = models.DateField()
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='student_profiles/', 
        blank=True, 
        null=True,
        help_text="Upload student profile picture"
    )
    
    # Academic Status
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('suspended', 'Suspended'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    # GPA tracking
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['student_id']  # Default ordering by student ID
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"
    
    def get_full_name(self):
        """Return the full name"""
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        """Return URL to student detail page"""
        return reverse('student_detail', kwargs={'pk': self.pk})
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))