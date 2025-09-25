# students/forms.py
from django import forms
from .models import Student
from accounts.models import User

class StudentForm(forms.ModelForm):
    """
    Form for creating and updating student information
    ModelForm automatically creates form fields based on model fields
    """
    
    class Meta:
        model = Student
        fields = [
            'student_id', 'first_name', 'last_name', 'email', 'phone_number',
            'department', 'year_of_admission', 'current_semester', 
            'date_of_birth', 'address', 'profile_picture', 'status', 'gpa'
        ]
        
        # Add Bootstrap CSS classes and HTML5 input types
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., ST2024001'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Computer Science'}),
            'year_of_admission': forms.NumberInput(attrs={'class': 'form-control', 'min': 2000, 'max': 2030}),
            'current_semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '4.00'}),
        }
        
        # Help texts for better UX
        help_texts = {
            'student_id': 'Unique identifier for the student (e.g., ST2024001)',
            'gpa': 'GPA on a 4.0 scale',
            'profile_picture': 'Upload a profile picture (optional)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make some fields required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['student_id'].required = True

class StudentSearchForm(forms.Form):
    """Form for searching students"""
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, student ID, or department...'
        })
    )
    
    department = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by department...'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + Student.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )