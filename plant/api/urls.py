from django.urls import path

# Importing related views
from . import views

# Setting up urls patterns
urlpatterns = [
    # Manufacturer related endpoints
    path('init/', views.InitPot),
    
    # User related endpoints
    path('register/', views.RegisterPot),
]