from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentCreationForm
# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile') # Redirect to the profile page after registration
    else:
        form = StudentCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')