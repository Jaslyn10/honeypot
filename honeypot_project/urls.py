from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('honeypot/', include('honeypot.urls')),  # Include honeypot URLs
    path('', lambda request: redirect('/honeypot/')),  # Redirect root to honeypot form
    
]
