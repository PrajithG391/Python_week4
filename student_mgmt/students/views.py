# students/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Student
from .forms import StudentForm, StudentSearchForm
from accounts.models import User

def admin_required(view_func):
    """Custom decorator to ensure only admin users can access certain views"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin():
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('student_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@admin_required
def student_list_view(request):
    """
    Display list of all students with search and pagination
    Only accessible by admin users
    """
    search_form = StudentSearchForm(request.GET)
    students = Student.objects.all()
    
    # Handle search functionality
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search')
        department_filter = search_form.cleaned_data.get('department')
        status_filter = search_form.cleaned_data.get('status')
        
        if search_query:
            # Search in multiple fields using Q objects (OR conditions)
            students = students.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(student_id__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        if department_filter:
            students = students.filter(department__icontains=department_filter)
        
        if status_filter:
            students = students.filter(status=status_filter)
    
    # Pagination - show 10 students per page
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_students': students.count(),
    }
    
    return render(request, 'students/student_list.html', context)

@login_required
@admin_required
def student_create_view(request):
    """Create a new student - Admin only"""
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)  # request.FILES for file uploads
        if form.is_valid():
            try:
                student = form.save()
                messages.success(request, f'Student {student.get_full_name()} created successfully!')
                return redirect('student_list')
            except Exception as e:
                messages.error(request, f'Error creating student: {str(e)}')
    else:
        form = StudentForm()
    
    context = {
        'form': form,
        'title': 'Add New Student',
        'button_text': 'Create Student'
    }
    return render(request, 'students/student_form.html', context)

@login_required
def student_detail_view(request, pk):
    """
    Display detailed information about a student
    Admin: can view any student
    Student: can only view their own profile
    """
    student = get_object_or_404(Student, pk=pk)
    
    # Permission check
    if not request.user.is_admin() and student.user != request.user:
        messages.error(request, 'You can only view your own profile.')
        return redirect('student_dashboard')
    
    context = {
        'student': student,
    }
    return render(request, 'students/student_detail.html', context)

@login_required
def student_update_view(request, pk):
    """
    Update student information
    Admin: can edit any student
    Student: can only edit their own profile
    """
    student = get_object_or_404(Student, pk=pk)
    
    # Permission check
    if not request.user.is_admin() and student.user != request.user:
        messages.error(request, 'You can only edit your own profile.')
        return redirect('student_dashboard')
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            try:
                updated_student = form.save()
                messages.success(request, f'Student {updated_student.get_full_name()} updated successfully!')
                
                # Redirect based on user role
                if request.user.is_admin():
                    return redirect('student_list')
                else:
                    return redirect('student_detail', pk=student.pk)
            except Exception as e:
                messages.error(request, f'Error updating student: {str(e)}')
    else:
        form = StudentForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
        'title': f'Edit {student.get_full_name()}',
        'button_text': 'Update Student'
    }
    return render(request, 'students/student_form.html', context)

@login_required
@admin_required
def student_delete_view(request, pk):
    """Delete a student - Admin only"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student_name = student.get_full_name()
        try:
            student.delete()
            messages.success(request, f'Student {student_name} deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting student: {str(e)}')
        return redirect('student_list')
    
    context = {
        'student': student,
    }
    return render(request, 'students/student_delete_confirm.html', context)

@login_required
def my_profile_view(request):
    """Student's own profile view - creates profile if doesn't exist"""
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        # If student profile doesn't exist, redirect to create one
        messages.info(request, 'Please complete your profile information.')
        return redirect('create_my_profile')
    
    return redirect('student_detail', pk=student.pk)

@login_required
def create_my_profile_view(request):
    """Allow students to create their own profile"""
    # Check if profile already exists
    try:
        student = request.user.student_profile
        messages.info(request, 'Your profile already exists.')
        return redirect('student_detail', pk=student.pk)
    except Student.DoesNotExist:
        pass  # Profile doesn't exist, continue with creation
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                student = form.save(commit=False)
                student.user = request.user  # Link to current user
                student.save()
                messages.success(request, 'Your profile has been created successfully!')
                return redirect('student_detail', pk=student.pk)
            except Exception as e:
                messages.error(request, f'Error creating profile: {str(e)}')
    else:
        # Pre-populate form with user data if available
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = StudentForm(initial=initial_data)
    
    context = {
        'form': form,
        'title': 'Create Your Profile',
        'button_text': 'Create Profile'
    }
    return render(request, 'students/student_form.html', context)