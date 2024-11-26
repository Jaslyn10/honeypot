from django.urls import path
from . import views

urlpatterns = [
    path('', views.honeypot_form, name='honeypot_form'),  # The form
    path('illegal-logs/', views.illegal_logs_view, name='illegal_logs'),
    path('submit/', views.honeypot_view, name='honeypot_view'),  # Form submission
]
