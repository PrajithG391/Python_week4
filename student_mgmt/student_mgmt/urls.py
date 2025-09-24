# student_mgmt/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# You will also need a view for the homepage/root URL
from django.shortcuts import render

def homepage_view(request):
    return render(request, 'homepage.html')

urlpatterns = [
    # Admin URL first
    path('admin/', admin.site.urls),

    # All of your app URLs go here
    path('accounts/', include('accounts.urls')),

    # A URL for the homepage (the root URL)
    path('', homepage_view, name='home'),
]

# The static and media file handlers MUST come at the end
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)