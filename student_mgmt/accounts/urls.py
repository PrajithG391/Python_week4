from django.urls import path
from . import views

urlpatterns = [
    # URL for the user registration page
    path('register/', views.register_view, name='register'),
    
    # URL for the user login page
    path('login/', views.login_view, name='login'),
    
    # URL for the user logout action
    path('logout/', views.logout_view, name='logout'),
    
    # URL for the user profile page (requires login)
    path('profile/', views.profile_view, name='profile'),
]