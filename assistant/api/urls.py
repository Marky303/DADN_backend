from django.urls import path

# Importing related views
from . import views

# Setting up urls patterns
urlpatterns = [
    # Manufacturer related endpoints
    path('prompt/', views.Chat),
    path('test/', views.TEST),
]