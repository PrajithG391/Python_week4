# student_mgmt/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

# A simple view for your homepage
def homepage_view(request):
    return render(request, 'homepage.html')

urlpatterns = [
    # 1. Django's admin URL
    path('admin/', admin.site.urls),

    # 2. Your custom app URLs (they MUST come before static files)
    path('accounts/', include('accounts.urls')),

    # 3. Your homepage URL
    path('', homepage_view, name='home'),
]

# 4. The URL patterns for serving static and media files go LAST
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)