# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, LoginForm
from .models import User

def home_view(request):
    """Home page view"""
    return render(request, 'home.html')

def register_view(request):
    """
    Handle student registration
    GET: Display registration form
    POST: Process form submission and create new user
    """
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create the user
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please login.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """
    Handle user login
    Session-based authentication: Django creates a session ID stored in cookies
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Verify credentials
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Create session
                messages.success(request, f'Welcome back, {username}!')
                # Redirect based on role
                if user.is_admin():
                    return redirect('admin_dashboard')
                else:
                    return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """Handle user logout - destroys session"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile_view(request):
    """
    Display user profile
    @login_required decorator ensures only logged-in users can access
    """
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def dashboard_view(request):
    """Redirect to appropriate dashboard based on role"""
    if request.user.is_admin():
        return redirect('admin_dashboard')
    return redirect('student_dashboard')

@login_required
def admin_dashboard_view(request):
    """Admin dashboard - only for admin users"""
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Admin only.')
        return redirect('student_dashboard')
    
    # Get statistics for dashboard
    total_students = User.objects.filter(role='student').count()
    context = {
        'total_students': total_students,
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
def student_dashboard_view(request):
    """Student dashboard - for student users"""
    return render(request, 'accounts/student_dashboard.html')